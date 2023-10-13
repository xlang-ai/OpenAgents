"""Implementation of the base webot calling chain."""
from __future__ import annotations

import re
import traceback
from typing import Dict, List, Optional

import json5
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
from pydantic import BaseModel, Extra

from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.web_agent.web_browsing.prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT,
)


class WebotCallingChain(Chain, BaseModel):
    """
    Basic prompt based webot call chain.

    The chain is initialized from a webot
    """

    llm_basic_chain: LLMChain

    memory: Optional[ReadOnlySharedStringMemory] = None  # fixme:
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
        return ["instruction", "start_url"]

    def parse_response(self, response: str):
        """Parse the endpoint and input_json"""
        instruction = None
        start_url = None
        success = False

        try:
            json_content = json5.loads(response)
            instruction = json_content["instruction"]
            start_url = json_content["start_url"]
            success = True
        except Exception:
            pattern = r"\```json\n(.+?)\n```" if "```json" in response else r"\```\n(.+?)\n```"
            match = re.search(pattern, response, re.DOTALL)

            if match:
                json_content = json5.loads(match.group(1))
                instruction = json_content["instruction"]
                start_url = json_content["start_url"]
                success = True
        if success:
            return {"instruction": instruction, "start_url": start_url }
        else:
            raise Exception("Parsing error")

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        input_str = inputs["input_str"]
        try:
            response_content = self.llm_basic_chain.run(**{"input_str": input_str})
            parsed_return = self.parse_response(response_content)
        except Exception as e:
            _run_manager.on_text(str(e) + "\n", color="red", verbose=self.verbose)
            _run_manager.on_text(traceback.format_exc(), color="red", verbose=self.verbose)

        return parsed_return

    @classmethod
    def create_basic_prompt(cls, system_prompt, user_prompt) -> BasePromptTemplate:
        # Call the LLM to get the predicted instruction and start_url
        input_variables = ["input_str"]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(user_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def from_llm(
        cls,
        llm: BaseLanguageModel,
    ) -> WebotCallingChain:
        llm_basic_chain = LLMChain(
            llm=llm,
            prompt=cls.create_basic_prompt(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=USER_PROMPT,
            ),
        )

        return cls(
            llm_basic_chain=llm_basic_chain,
        )
