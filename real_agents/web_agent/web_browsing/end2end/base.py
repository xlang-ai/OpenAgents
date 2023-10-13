"""Implementation for prompt based end2end web bots."""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional
from loguru import logger
from pydantic import BaseModel, Extra

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.web_agent.web_browsing.end2end.prompt import (
    RETRY_PROMPT,
    SYSTEM_PROMPT,
    USER_PROMPT,
)
from real_agents.web_agent.web_browsing.schema import ACTIONS
from real_agents.adapters.data_model.html import HTMLDataModel


class WebotChain(Chain, BaseModel):
    """Basic prompt based web bot that interact with websites. This implementation is highly motivated by Taxy.ai"""

    llm_basic_chain: LLMChain
    llm_retry_chain: LLMChain

    memory: Optional[ReadOnlySharedStringMemory] = None
    output_key: str = "action"

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
        return ["user_query", "previous_actions", "page_info"]

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.

        :meta private:
        """
        return [self.output_key]

    @property
    def formatted_actions(self) -> str:
        formatted_actions = ""
        for i, action in enumerate(ACTIONS):
            args_str = ""
            for arg in action["args"]:
                if args_str != "":
                    args_str += ", "
                args_str += f'{arg["name"]}: {arg["type"]}'
            formatted_action = f"{i + 1}. {action['name']}({args_str}): {action['description']}"
            if formatted_actions != "":
                formatted_actions += "\n"
            formatted_actions += formatted_action
        return formatted_actions

    def parse_response(self, text):
        class Argument:
            def __init__(self, name, arg_type):
                self.name = name
                self.type = arg_type

        class Action:
            def __init__(self, name, description, args):
                self.name = name
                self.description = description
                self.args = [Argument(arg["name"], arg["type"]) for arg in args]

        available_actions = [
            Action("click", "Clicks on an element", [{"name": "elementId", "type": "number"}]),
            Action(
                "setValue",
                "Focuses on and sets the value of an input element",
                [{"name": "elementId", "type": "number"}, {"name": "value", "type": "string"}],
            ),
            Action("finish", "Indicates the task is finished", []),
            Action("fail", "Indicates that you are unable to complete the task", []),
        ]
        thought_match = re.search("<Thought>(.*?)</Thought>", text)
        action_match = re.search("<Action>(.*?)</Action>", text)

        if thought_match is None:
            return {"error": "Invalid response: Thought not found in the model response."}

        if action_match is None:
            return {"error": "Invalid response: Action not found in the model response."}

        thought = thought_match.group(1)
        action_string = action_match.group(1)
        action_pattern = re.compile("(\w+)\((.*?)\)")
        action_parts = action_pattern.match(action_string)

        if action_parts is None:
            return {"error": "Invalid action format: Action should be in the format functionName(arg1, arg2, ...)."}

        action_name = action_parts.group(1)
        action_args_string = action_parts.group(2)

        available_action = next((action for action in available_actions if action.name == action_name), None)

        if available_action is None:
            return {"error": f'Invalid action: "{action_name}" is not a valid action.'}

        args_array = [arg.strip() for arg in action_args_string.split(",") if arg.strip() != ""]
        parsed_args = {}

        if len(args_array) != len(available_action.args):
            return {
                "error": f'Invalid number of arguments: Expected {len(available_action.args)} for action "{action_name}", but got {len(args_array)}.'
            }

        for i in range(len(args_array)):
            arg = args_array[i]
            expected_arg = available_action.args[i]

            if expected_arg.type == "number":
                try:
                    number_value = int(arg)
                    parsed_args[expected_arg.name] = number_value
                except ValueError:
                    return {
                        "error": f'Invalid argument type: Expected a number for argument "{expected_arg.name}", but got "{arg}".'
                    }
            elif expected_arg.type == "string":
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    parsed_args[expected_arg.name] = arg[1:-1]
                else:
                    return {
                        "error": f'Invalid argument type: Expected a string for argument "{expected_arg.name}", but got "{arg}".'
                    }
            else:
                return {
                    "error": f'Invalid argument type: Unknown type "{expected_arg.type}" for argument "{expected_arg.name}".'
                }

        parsed_action = {"name": available_action.name, "args": parsed_args}

        return {"thought": thought, "action": action_string, "parsedAction": parsed_action}

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        logger.bind(msg_head="WebotChain inputs").trace(inputs)

        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        # Get  ["user_query", "previous_actions", "page_info"], and other raw data
        plan = inputs["plan"]
        previous_actions = inputs["previous_actions"]
        user_query = inputs["user_query"]
        page_info = inputs["page_info"]
        
        model = HTMLDataModel.from_raw_data(page_info)
        processed_html = model.get_llm_side_data()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate the prompt
        previous_actions_string = "\n".join(["<Action>{}</Action>".format(action) for action in previous_actions])

        user_prompt = f"The user requests the following task:\n {user_query}\n{previous_actions_string}\nCurrent time: {current_time}\nCurrent page contents:\n{processed_html}"
        
        print("user_prompt",user_prompt)

        action = self.llm_basic_chain.run(
            **{
                "formattedActions": self.formatted_actions,
                "plan": plan,
                "user_query": user_query,
                "previous_actions_string": previous_actions_string,
                "current_time": current_time,
                "processed_html": processed_html,
            }
        )

        # Extract from "<Action>{}</Action>"
        parsed_return = self.parse_response(action)
        print("parsed_return",parsed_return)
        retry_count = 0
        while "error" in parsed_return and retry_count < 5:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            action = self.retry(user_query, previous_actions_string, current_time, page_info, action)
            retry_count += 1
            previous_actions_string += "\n" + action
            parsed_return = self.parse_response(action)

        parsed_action = parsed_return["parsedAction"]

        logger.bind(msg_head="WebotChain generated action").trace(parsed_action)

        return parsed_return

    def retry(self, plan, user_query, previous_actions_string, current_time, page_info: str, last_action: str) -> str:
        action = self.llm_retry_chain.run(
            **{
                "formattedActions": self.formatted_actions,
                "plan": plan,
                "user_query": user_query,
                "previous_actions_string": previous_actions_string,
                "current_time": current_time,
                "processed_html": page_info,
                "last_action": last_action,
            }
        )
        return action

    @classmethod
    def create_basic_prompt(cls, system_prompt, user_prompt) -> BasePromptTemplate:
        # Call the LLM to get the predicted end_point and input_json
        input_variables = [
            "formattedActions",
            "plan",
            "user_query",
            "previous_actions_string",
            "current_time",
            "processed_html",
        ]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(user_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def create_retry_prompt(cls, system_prompt, retry_prompt) -> BasePromptTemplate:
        # Call the LLM to get the predicted end_point and input_json in retry
        input_variables = [
            "formattedActions",
            "plan",
            "user_query",
            "previous_actions_string",
            "current_time",
            "processed_html",
            "retry_message",
        ]
        messages = [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(retry_prompt),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, **kwargs: Any) -> WebotChain:
        """Load from the initial web page and user instruction"""
        llm_basic_chain = LLMChain(
            llm=llm,
            prompt=cls.create_retry_prompt(
                system_prompt=SYSTEM_PROMPT,
                retry_prompt=USER_PROMPT,
            ),
        )

        llm_retry_chain = LLMChain(
            llm=llm,
            prompt=cls.create_retry_prompt(
                system_prompt=SYSTEM_PROMPT,
                retry_prompt=RETRY_PROMPT,
            ),
        )

        return cls(
            llm_basic_chain=llm_basic_chain,
            llm_retry_chain=llm_retry_chain,
            **kwargs,
        )
