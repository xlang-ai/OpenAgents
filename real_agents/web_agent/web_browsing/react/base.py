"""Implementation for prompt based react web bots."""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional, Tuple
from loguru import logger

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.llm import LLMChain

from real_agents.web_agent.web_browsing.end2end.base import WebotChain
from real_agents.web_agent.web_browsing.react.prompt import (
    RETRY_PROMPT,
    SYSTEM_PROMPT,
    USER_PROMPT,
)

class ReActWebotChain(WebotChain):
    """Basic prompt based web bot that interact with websites."""

    max_retry_times: int = 3

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.

        :meta private:
        """
        return ["plan", "user_query", "previous_actions", "previous_thoughts", "page_info"]

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.

        :meta private:
        """
        # success: boolean, message: string, action: string, thought: string
        # success is a boolean indicating whether the action was successful
        # message is the error message that will be displayed to the user if success == false
        # example: {'success': True, 'message' = 'success', 'thought': "I should first set the value in the search field to '...'", 'action': 'setValue(93, "...")', 'parsedAction': {'name': 'setValue', 'args': {'elementId': 93, 'value': '...'}}}
        return ["success", "message", "action", "thought", "parsedAction"]

    #example case: _format_error_output({"error": "This model's maximum context length is 8192 tokens. However, your messages resulted in 8243 tokens. Please reduce the length of the messages."})
    #you need to input like the example, i.e. stringfy the error thrown and put it in a dict with the key "error"
    def _format_error_output(self, error_output: Dict[str, str]) -> Dict[str, Any]:
        return {
            "success": False,
            "message": error_output["error"],
            "action": "error",
            "thought": error_output["error"],
            "parsedAction": {"name": "error", "args": {}},
        }

    def parse_response(self, text):
        if "finish" in text:
            thought_match = re.search("<Thought>(.*?)</Thought>", text)
            if thought_match is None:
                return self._format_error_output({"error": "Invalid response: Thought not found in the model response."})
            thought = thought_match.group(1)
            action_string = "finish"
            parsed_action = "finish"
            return {"thought": thought, "action": action_string, "parsedAction": {"name": "finish", "args": {}}}

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
                "Focuses on and sets the value of an input element. Must set a proper value which aligns to the user's request and the function of the input box.",
                [{"name": "elementId", "type": "number"}, {"name": "value", "type": "string"}],
            ),
            Action("finish", "Indicates the task is finished(i.e. the info in the new page is enough for user's request or the task has been successfully completed).", []),
            Action("fail", "Indicates that you are unable to complete the task", []),
        ]
        thought_match = re.search("<Thought>\s*(.*?)\s*</Thought>", text)
        action_match = re.search("<Action>\s*(.*?)\s*</Action>", text)

        if thought_match is None:
            return self._format_error_output({"error": "Invalid response: Thought not found in the model response."})

        if action_match is None:
            return self._format_error_output({"error": "Invalid response: Action not found in the model response."})

        thought = thought_match.group(1)
        action_string = action_match.group(1)
        action_pattern = re.compile("(\w+)\((.*?)\)")
        action_parts = action_pattern.match(action_string)

        if action_parts is None:
            return self._format_error_output({"error": "Invalid action format: Action should be in the format functionName(arg1, arg2, ...)."})

        action_name = action_parts.group(1)
        action_args_string = action_parts.group(2)

        available_action = next((action for action in available_actions if action.name == action_name), None)

        if available_action is None:
            return self._format_error_output({"error": f'Invalid action: "{action_name}" is not a valid action.'})

        # split by "," but only split in the first instance
        args_array = [arg.strip() for arg in action_args_string.split(",", 1) if arg.strip() != ""]
        parsed_args = {}

        if len(args_array) != len(available_action.args):
            return self._format_error_output({
                "error": f'Invalid number of arguments: Expected {len(available_action.args)} for action "{action_name}", but got {len(args_array)}.'
            })

        for i in range(len(args_array)):
            arg = args_array[i]
            expected_arg = available_action.args[i]

            if expected_arg.type == "number":
                try:
                    number_value = int(arg)
                    parsed_args[expected_arg.name] = number_value
                except ValueError:
                    return self._format_error_output({
                        "error": f'Invalid argument type: Expected a number for argument "{expected_arg.name}", but got "{arg}".'
                    })
            elif expected_arg.type == "string":
                match_single = re.match(r"^'((?:[^']|\\')*)'$", arg)
                match_double = re.match(r'^"((?:[^"]|\\")*)"$', arg)
                if match_single is not None:
                    parsed_args[expected_arg.name] = match_single.group(1)
                elif match_double is not None:
                    parsed_args[expected_arg.name] = match_double.group(1)
                else:
                    return self._format_error_output({
                        "error": f'Invalid argument type: Expected a string for argument "{expected_arg.name}", but got "{arg}".'
                    })
            else:
                return self._format_error_output({
                    "error": f'Invalid argument type: Unknown type "{expected_arg.type}" for argument "{expected_arg.name}".'
                })

        parsed_action = {"name": available_action.name, "args": parsed_args}

        return {"thought": thought, "action": action_string, "parsedAction": parsed_action}
    
    # check the validity of the action, if ok, return (True, ""), else return (False, error message)
    def _check_valid_action(self, html: str, parsed_return: dict) -> Tuple(bool, str):
        parsedAction = parsed_return["parsedAction"]
        action = parsed_return["action"]
        retry_message = ""
        
        # check if the element id exists in the html (fixme: maybe more validity checking methods can be applied)
        if parsedAction["name"] == "click":
            elementId = parsedAction["args"].get("elementId", None)
            if elementId != None and str(elementId) in html:
                return True, ""
            else:
                retry_message = "The elementId of your last action does not exist in the html, please try again."
                return False, retry_message
        elif parsedAction["name"] == "setValue":
            elementId = parsedAction["args"].get("elementId", None)
            value = parsedAction["args"].get("value", None)
            if elementId != None and value != None and str(elementId) in html:
                return True, ""
            else:
                retry_message = "The elementId of your last action does not exist in the html, please try again."
                return False, retry_message
        elif "finish" in parsedAction["name"]:
            return True, ""
        elif "fail" in parsedAction["name"]:
            return True, ""
        elif "interrupt" in parsedAction["name"]:
            return True, ""
        # parse error
        elif "error" in parsedAction["name"]:
            retry_message = "Action parse error, please follow the output format and try again."
            return False, retry_message
        else:
            retry_message = "Action not in available actions, please try again."
            return False, retry_message

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # logger.bind(msg_head="ReActWebotChain inputs").trace(inputs)

        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()

        # Get  ["user_query", "previous_actions", "previous_thoughts", "page_info"], and other raw data
        plan = inputs["plan"]
        previous_actions = inputs["previous_actions"]
        previous_thoughts = inputs["previous_thoughts"]
        user_query = inputs["user_query"]
        processed_html = inputs["page_info"]

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate the prompt
        previous_actions_string = "\n".join(
            [
                "<Thought>{}</Thought>\n<Action>{}</Action>".format(thought, action)
                for thought, action in zip(previous_thoughts, previous_actions)
            ]
        )
        if len(previous_actions_string) > 0:
            previous_actions_string  = "You have already taken the following thoughts and actions:\n"+previous_actions_string

        user_prompt = f"The user requests the following task:\n {user_query}\nyou have taken these{previous_actions_string}\nCurrent time: {current_time}\nCurrent page contents:\n{processed_html}"
        # print(user_prompt)

        valid_action = False
        count = 0
        retry_message = ""

        while not valid_action and count < self.max_retry_times:
            try:
                if count == 0:
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
                else:
                    action = self.llm_retry_chain.run(
                    **{
                        "formattedActions": self.formatted_actions,
                        "plan": plan,
                        "user_query": user_query,
                        "previous_actions_string": previous_actions_string,
                        "current_time": current_time,
                        "processed_html": processed_html,
                        "retry_message": retry_message,
                    }
                )
            except Exception as e:
                print("*"*50)
                print("llm error:",e)
                print("*"*50)
                error_output = {"error": str(e)}
                return self._format_error_output(error_output)

            # print("llm output:",action)

            # Extract from "<Thought>{}</Thought>\n<Action>{}</Action>"
            action = action.split("</Action>")[0] + "</Action>"
            # action: <Thought>I should first set the value in the search field to '...'</Thought>
            #         <Action>setValue(93, "Tao Yu")</Action>
            # print("action:",action)

            # parsed return: {'thought': "I should first set the value in the search field to '...'", 'action': 'setValue(93, "...")', 'parsedAction': {'name': 'setValue', 'args': {'elementId': 93, 'value': '...'}}}
            parsed_return = self.parse_response(action)

            # If parse error, there will be  "success" and "message" key in parsed_return. If no problem, no "success" and "message" key. set its value by setdefault
            parsed_return.setdefault("success", True)
            parsed_return.setdefault("message", "success")

            valid_action, retry_message = self._check_valid_action(processed_html, parsed_return)
            
        # if "error" not in parsed_return:
            # logger.bind(msg_head="ReActWebotChain generated thought").trace(parsed_return["thought"])
            # logger.bind(msg_head="ReActWebotChain generated action").trace(parsed_return["parsedAction"])

        output = parsed_return

        return output

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, **kwargs: Any) -> WebotChain:
        """Load from the initial web page and user instruction"""
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

        return cls(
            llm_basic_chain=llm_basic_chain,
            llm_retry_chain=llm_retry_chain,
            **kwargs,
        )
