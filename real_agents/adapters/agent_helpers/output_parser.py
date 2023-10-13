from __future__ import annotations

from typing import Optional, Union
from pydantic import Extra

from langchain.schema import (
    AgentAction,
    AgentFinish,
)
from real_agents.adapters.agent_helpers.agent import AgentOutputParser
from real_agents.adapters.schema import AgentTransition


class ConversationOutputParser(AgentOutputParser):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.allow
        arbitrary_types_allowed = True

    def get_format_instructions(self, app_name="copilot") -> str:
        from real_agents.data_agent.copilot_prompt import FORMAT_INSTRUCTIONS as COPILOT_FORMAT_INSTRUCTIONS
        from real_agents.plugins_agent.plugin_prompt import FORMAT_INSTRUCTIONS as PLUGINS_FORMAT_INSTRUCTIONS
        from real_agents.web_agent.webot_prompt import FORMAT_INSTRUCTIONS as WEBOT_FORMAT_INSTRUCTIONS

        if app_name == "copilot":
            return COPILOT_FORMAT_INSTRUCTIONS
        elif app_name == "webot":
            return WEBOT_FORMAT_INSTRUCTIONS
        elif app_name == "plugins":
            return PLUGINS_FORMAT_INSTRUCTIONS
        else:
            raise ValueError(f"Unknown app_name {app_name}")

    def parse(self, text: str) -> Union[AgentTransition, AgentAction, AgentFinish]:
        cleaned_output = text.strip()
        import re

        def _extract_explanation(json_string: str) -> Optional[str]:
            if "```" in json_string:
                return json_string.split("```")[0]
            else:
                return None

        def _extract_value(json_string: str, key: str) -> str:
            pattern = re.compile(rf'"?{key}"?\s*:\s*("((?:[^"\\]|\\.)*)"|(\b[^,\s]*\b))', re.MULTILINE)
            match = pattern.search(json_string)
            if match:
                return match.group(1).replace('\\"', '"').replace("\\\\", "\\").strip('"').strip("'")

            raise ValueError(f"Could not find {key} in {json_string}")

        try:
            _action = _extract_value(cleaned_output, "action")
            _action_input = _extract_value(cleaned_output, "action_input")
            if _action == "Final Answer":
                return AgentFinish({"output": _action_input}, cleaned_output)

            # Transition sentence should only be used not final answer.
            _explanation = _extract_explanation(cleaned_output)
            return AgentAction(_action, _action_input, cleaned_output)
        except Exception:
            if cleaned_output.startswith("Action:"):
                lines = cleaned_output.splitlines()
                action = lines[1].strip()
                import textwrap

                action_input = textwrap.dedent("\n".join(lines[2:])).strip()
                return AgentAction(action, action_input, cleaned_output)

            return AgentFinish({"output": cleaned_output}, cleaned_output)

    @property
    def _type(self) -> str:
        return "conversational_chat"
