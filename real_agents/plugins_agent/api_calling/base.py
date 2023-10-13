"""Implement API calling."""

from __future__ import annotations

import re
import traceback
from typing import Any, Callable, Dict, List, Optional
import backoff
import json5
from fuzzywuzzy import process
from pydantic import BaseModel, Extra

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from real_agents.plugins_agent.api_calling.custom_exceptions import ParsingError, \
    APICallingError
from real_agents.adapters.data_model import SpecModel
from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.plugins_agent.api_calling.prompt import (
    RETRY_PROMPT,
    STOP_PROMPT,
    SYSTEM_PROMPT,
    USER_PROMPT,
)


class APICallingChain(Chain, BaseModel):
    """Chain for Calling API"""

    llm_basic_chain: LLMChain
    llm_retry_chain: LLMChain
    llm_stop_chain: LLMChain

    meta_info: Dict[str, Any]
    spec_model: SpecModel
    endpoint2caller: Dict[str, Callable]
    endpoint2output_model: Dict[str, Callable]
    api_key: Optional[str] = None

    memory: Optional[ReadOnlySharedStringMemory] = None  # fixme:
    retry_times = 1
    stop: str = "\n\n"
    verbose = True

    chat_id: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.

        :meta private:
        """
        return ["input_str"]

    @property
    def output_keys(self) -> List[str]:
        """Return the output keys.

        :meta private:
        """
        return ["endpoint", "input_json", "api_output"]

    @property
    def specs_str(self):
        """The str representation of spec."""
        return "\n".join(
            [
                f"{i}.\n{self.spec_model.prepare_spec_for_one_path(p, include_api_info=False)}"
                for i, p in enumerate(self.spec_model.paths.keys())
            ]
        )

    @property
    def need_auth(self):
        """Whether the API call needs authentication."""
        return not self.meta_info["manifest"]["auth"]["type"] in [
            None,
            "None",
            "none",
            "Null",
            "null",
        ]  # the value of type is not null in ai-plugin.json

    @backoff.on_exception(backoff.expo, Exception, max_tries=10, max_time=20)
    def call_api(self, endpoint, input_json):
        """Call the API and return the output. Wrap the data in the output model."""
        # Find the endpoint by fuzzy match, in case sometimes LLM generated a wrong endpoint
        if endpoint not in self.endpoint2caller:
            return "Endpoint not found. Please try again."

        endpoint = process.extractOne(endpoint, list(self.endpoint2caller.keys()))[0]

        # Add fuzzy match for endpoint
        try:
            api_output = (
                self.endpoint2caller[endpoint](input_json, self.api_key)
                if self.need_auth
                else self.endpoint2caller[endpoint](input_json)
            )
        except Exception as e:
            raise APICallingError(f"{e}")

        compressed_output = self.endpoint2output_model[endpoint]({"out": api_output})[
            "out"]
        return compressed_output

    def parse_response(self, response: str):
        """Parse the endpoint and input_json"""
        endpoint = None
        input_json = None

        try:
            json_content = json5.loads(response)
            endpoint = json_content["endpoint"]
            input_json = json_content["input_json"]
        except:
            pattern = r"```json\n(.+?)\n```" if "```json" in response else r"```\n(.+?)\n```"
            match = re.search(pattern, response, re.DOTALL)

            if match:
                try:
                    json_content = json5.loads(match.group(1))
                    endpoint = json_content["endpoint"]
                    input_json = json_content["input_json"]
                except Exception as e:
                    raise ParsingError(f"{e}")

        # When the endpoint is null, we use the default endpoint
        if endpoint is None or endpoint == "null" or endpoint == "Null" or endpoint == "NULL":
            endpoint = "\\"

        return {"endpoint": endpoint, "input_json": input_json}

    @classmethod
    def create_basic_prompt(cls, system_prompt, user_prompt) -> BasePromptTemplate:
        # Call the LLM to get the predicted end_point and input_json
        input_variables = ["specs_str", "input_str"]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(user_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def create_retry_prompt(cls, system_prompt, retry_prompt) -> BasePromptTemplate:
        # Call the LLM to get the predicted end_point and input_json in retry
        input_variables = ["specs_str", "input_str", "trial_history"]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(retry_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def create_stop_prompt(cls, system_prompt, stop_prompt) -> BasePromptTemplate:
        # Decide the stop when the LLM are getting the predicted end_point and input_json
        input_variables = ["specs_str", "input_str", "api_output"]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(stop_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    def retry(self, input_str: str, trial_history: List[Dict],
              _run_manager: CallbackManagerForChainRun,
              vars_to_pass: Dict) -> None:
        response_content = (
            self.llm_basic_chain.run(
                **{"specs_str": self.specs_str, "input_str": input_str})
            if len(trial_history) == 0
            else self.llm_retry_chain.run(
                **{"specs_str": self.specs_str, "input_str": input_str,
                   "trial_history": trial_history}
            )
        )

        parsed_return = self.parse_response(response_content)

        _run_manager.on_text(parsed_return, indent=4, color="green",
                             verbose=self.verbose)

        endpoint, input_json = (
            parsed_return["endpoint"],
            parsed_return["input_json"],
        )

        vars_to_pass["endpoint"] = endpoint
        vars_to_pass["input_json"] = input_json

        api_output = self.call_api(endpoint, input_json)
        vars_to_pass["api_output"] = api_output

        _run_manager.on_text(api_output, color="yellow", verbose=self.verbose)

        should_stop = (
                self.llm_stop_chain.run(
                    **{"specs_str": self.specs_str, "input_str": input_str,
                       "api_output": api_output})
                .lower()
                .strip()
                == "yes"
        )
        _run_manager.on_text(should_stop, color="yellow", verbose=self.verbose)
        vars_to_pass["should_stop"] = should_stop

    def _call(
            self,
            inputs: Dict[str, str],
            run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        input_str = inputs["input_str"]

        trial_history = []
        count = 0
        vars_to_pass = {"endpoint": None, "input_json": None, "api_output": None,
                        "should_stop": False}

        while count < self.retry_times:
            try:
                self.retry(input_str, trial_history, _run_manager, vars_to_pass)
                trial_history.append({"input_json": vars_to_pass["input_json"],
                                      "api_output": vars_to_pass["api_output"]})
                if vars_to_pass["should_stop"]:
                    break
                else:
                    count += 1
            except ParsingError as e:
                _run_manager.on_text(str(e) + "\n", color="red", verbose=self.verbose)
                trial_history.append({"errors": str(e)})
                count += 1
                continue
            except APICallingError as e:
                _run_manager.on_text(str(e) + "\n", color="red", verbose=self.verbose)
                trial_history.append({"errors": str(e)})
                count += 1
                continue
            except Exception as e:
                # fixme: Handle the exception, make error message shorter
                _run_manager.on_text(str(e) + "\n", color="red", verbose=self.verbose)
                _run_manager.on_text(traceback.format_exc(), color="red",
                                     verbose=self.verbose)
                trial_history.append({"errors": str(e)})
                count += 1
                continue

        if count == self.retry_times:
            if "errors" in trial_history[-1]:
                return {"endpoint": vars_to_pass["endpoint"],
                        "input_json": vars_to_pass["input_json"],
                        "api_output": trial_history[-1]["errors"]}
            else:
                return {"endpoint": vars_to_pass["endpoint"]} | (
                    trial_history[-1])  # return the last trial history
        else:
            return {"endpoint": vars_to_pass["endpoint"],
                    "input_json": vars_to_pass["input_json"],
                    "api_output": vars_to_pass["api_output"]}

    @classmethod
    def from_llm_and_plugin(
            cls,
            llm: BaseLanguageModel,
            meta_info: Dict[str, Any],
            spec_model: SpecModel,
            endpoint2caller: Dict[str, Callable],
            endpoint2output_model: Dict[str, Callable],
            api_key: str,
    ) -> APICallingChain:
        llm_basic_chain = LLMChain(
            llm=llm,
            prompt=cls.create_basic_prompt(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=USER_PROMPT,
            ),
        )

        llm_retry_chain = LLMChain(
            llm=llm,
            prompt=cls.create_retry_prompt(
                system_prompt=SYSTEM_PROMPT,
                retry_prompt=RETRY_PROMPT,
            ),
        )
        llm_stop_chain = LLMChain(
            llm=llm,
            prompt=cls.create_stop_prompt(
                system_prompt=SYSTEM_PROMPT,
                stop_prompt=STOP_PROMPT,
            ),
        )

        return cls(
            llm_basic_chain=llm_basic_chain,
            llm_retry_chain=llm_retry_chain,
            llm_stop_chain=llm_stop_chain,
            meta_info=meta_info,
            spec_model=spec_model,
            endpoint2caller=endpoint2caller,
            endpoint2output_model=endpoint2output_model,
            api_key=api_key,
        )
