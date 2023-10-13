"""
Implementation of the WebBrowsingExecutor.
WebBrowsingExecutor takes start_url and instruction as input, iteratively perform the actions on the web, and return the result.
"""
from typing import Any, Dict, List

from langchain.base_language import BaseLanguageModel

from real_agents.web_agent.web_browsing.react.base import ReActWebotChain
from real_agents.web_agent.web_browsing.end2end.base import WebotChain
from real_agents.adapters.data_model.html import HTMLDataModel


# This executor is for the extension usage and not for the chat interface.
# For the chat interface webot executor, refer xlang/real_agents/web_agent/executors/web_browsing_executor.py
class WebBrowsingExecutor:
    """
    WebBrowsingExecutor takes start_url and instruction as input, iteratively perform the actions on the web, and return the result.
    """

    def __init__(self, instruction: str, plan: str = "", mode: str = "react") -> None:
        """Initialize the executor"""
        self.instruction: str = instruction
        self.mode: str = mode
        if self.mode == "react":
            self.thoughts_taken: List[str] = []
        self.actions_taken: List[str] = []
        self.pages_viewed: List[Any] = []
        self.plan: str = plan

    @property
    def finish(self):
        return True if len(self.actions_taken) > 0 and "finish" in self.actions_taken[-1] else False

    @property
    def interrupt(self):
        return True if len(self.actions_taken) > 0 and "interrupt" in self.actions_taken[-1] else False

    @property
    def error(self):
        return True if len(self.actions_taken) > 0 and "error" in self.actions_taken[-1] else False

    @property
    def fail(self):
        return True if len(self.actions_taken) > 0 and "fail" in self.actions_taken[-1] else False

    @property
    def action_history(self):
        if self.mode == "basic":
            action_history = "Action: "
            for action in self.actions_taken:
                action_history += action + " -> "
            return action_history
        elif self.mode == "react":
            action_history = ""
            for thought, action in zip(self.thoughts_taken, self.actions_taken):
                action_history += thought + " -> " + action + " -> "
            return action_history
        else:
            raise ValueError(f"The mode {self.mode} is not supported")

    def run(
            self,
            page_info: Any,
            llm: BaseLanguageModel,
    ) -> Dict[str, Any]:
        model = HTMLDataModel.from_raw_data(raw_data=page_info)
        processed_html = model.get_llm_side_data()
        if self.mode == "basic":
            method = WebotChain.from_llm(llm)
            self.pages_viewed.append(processed_html)
            action_element = method(
                {"user_query": self.instruction, "previous_actions": self.actions_taken, "page_info": processed_html}
            )
        elif self.mode == "react":
            method = ReActWebotChain.from_llm(llm)
            self.pages_viewed.append(processed_html)
            print("self.plan:", self.plan)

            # example: {'success': True, 'message' = 'success', 'thought': "I should first set the value in the search field to '...'", 'action': 'setValue(93, "...")', 'parsedAction': {'name': 'setValue', 'args': {'elementId': 93, 'value': '...'}}}
            webot_chain_return = method(
                {
                    "user_query": self.instruction,
                    "plan": self.plan,
                    "previous_actions": self.actions_taken,
                    "previous_thoughts": self.thoughts_taken,
                    "page_info": processed_html,
                }
            )
        else:
            raise ValueError(f"The mode {self.mode} is not supported")

        # "I should first set the value in the search field to '...'"
        self.thoughts_taken.append(webot_chain_return["thought"])

        # setValue(93, "...")
        self.actions_taken.append(webot_chain_return["action"])

        print("actions_taken:", self.actions_taken)
        return webot_chain_return
