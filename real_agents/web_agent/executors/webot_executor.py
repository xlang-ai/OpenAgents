"""
Implementation of the WebotExecutor class.
WebotExecutor takes user's intent as input, return the start_url and instruction as the input for web browsing plugin
"""
from __future__ import annotations

from typing import Any, Dict, Union

from langchain.base_language import BaseLanguageModel
from pydantic import BaseModel, Extra

from real_agents.web_agent.web_browsing.base import WebotCallingChain


# This executor is for chat interface usage and not for the extension usage.
# For the extension usage, refer to xlang/real_agents/web_agent/executors/web_browsing_executor.py
class WebotExecutor(BaseModel):
    """
    WebotExecutor takes user's intent as input, return the start_url and instruction as the input for web browsing plugin (tool).
    """
    name: str
    description: str

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @classmethod
    def from_webot(cls) -> WebotExecutor:
        return cls(
            name="WeBot",
            description="Use the web navigation agent to perform actions on the web, including information retrieval, task completion(e.g. write an email or tweet or organize a meeting), etc. The action input should contain the action and the start url.\For example:\nUse xxx.com to search xxx.",
        )

    def run(
            self,
            user_intent: str,
            llm: BaseLanguageModel,
    ) -> Union[str, Dict[str, Any]]:
        inputs = {"input_str": user_intent}
        method = WebotCallingChain.from_llm(
            llm,
        )
        output = method(inputs)
        return output
