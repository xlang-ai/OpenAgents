import re
import textwrap
from typing import List, Dict, Any, Optional
from langchain.schema import BaseMessage
import tiktoken

# format of agent action
ACTION_FORMAT = """```json
{{
    "action": "{_action}",
    "action_input": "{_action_input}",
}}
```"""

# format of tool call(code) & tool output(response)
TOOL_FORMAT = {
    "code": """<code>
{_intermediate_steps}
</code>

<output>
{_result}
</output>
""",
    "plugin": """<plugin_call>
{_intermediate_steps}
</plugin_call>

<output>
{_result}
</output>
""",
}

# format to wrap tool call + tool output together
TOOL_RESPONSE_FORMAT = """[RESPONSE_BEGIN]
{_response}
[RESPONSE_END]
"""


class MessageDataModel:
    """A data model for Message Management, general purpose."""

    @staticmethod
    def _count_tokens(test_string: str) -> int:
        """copy of langchain _get_num_token_default_method"""
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = len(enc.encode(test_string))
        return tokens

    @classmethod
    def _get_num_tokens_from_messages(cls, buffer: List[BaseMessage]) -> int:
        return sum([cls._count_tokens(m.content) for m in buffer])

    @classmethod
    def truncate_text(cls, raw_text: str, max_token: Optional[int] = 250, trunc_ratio: int = 0.5) -> str:
        """heuristic truncation for single long string & code"""
        tokens = cls._count_tokens(raw_text)
        if max_token is None or tokens <= max_token:
            return raw_text

        # assume we keep the first ratio * max_tokens and the (1 - ratio) * max_tokens
        half_tokens = int(max_token * trunc_ratio)
        lines = raw_text.strip().split("\n")
        lines = [" ".join(line.split(" ")[:100]) for line in lines]
        total_lines = len(lines)

        # first half
        left = 0
        right = total_lines // 2
        while left < right:
            mid = (left + right) >> 1
            text = "\n".join(lines[0:mid])
            token = cls._count_tokens(text)
            if token > half_tokens:
                right = mid
            else:
                left = mid + 1
        first_half = "\n".join(lines[0:right])

        # last half
        left = total_lines // 2 + 1
        right = total_lines - 1
        while left < right:
            mid = (left + right) >> 1
            text = "\n".join(lines[mid:])
            token = cls._count_tokens(text)
            if token > half_tokens:
                right = mid
            else:
                left = mid + 1
        second_half = "\n".join(lines[left:])

        if first_half != "" or second_half != "":
            return f"{first_half}\n...\n[too long to show]\n...\n{second_half}"
        else:
            # if len(first_half_list) == 0 and len(last_half_list) == 0:
            # if all lines >= max_token, return last 100 words as truncated results.
            return f"...\n[too long to show]\n...\n{raw_text[-100:]}"

    @classmethod
    def truncate_chat_history(cls, full_inputs: Dict[str, Any], max_token: int = 2500) -> Dict[str, Any]:
        _input = full_inputs["input"]
        agent_scratchpad = full_inputs["agent_scratchpad"]
        agent_scratchpad = "\n".join([_.content for _ in agent_scratchpad])
        _input_tokens = cls._count_tokens(_input)
        _scratchpad_tokens = cls._count_tokens(agent_scratchpad)

        left_tokens = max_token - _scratchpad_tokens - _input_tokens
        chat_history = full_inputs["chat_history"]

        curr_buffer_length = cls._get_num_tokens_from_messages(chat_history)
        while len(chat_history) != 0 and curr_buffer_length > left_tokens:
            chat_history.pop(0)
            curr_buffer_length = cls._get_num_tokens_from_messages(chat_history)
        full_inputs["chat_history"] = chat_history
        return full_inputs

    @staticmethod
    def _extract_value(json_string: str, key: str) -> str:
        pattern = re.compile(rf'"?{key}"?\s*:\s*("((?:[^"\\]|\\.)*)"|(\b[^,\s]*\b))', re.MULTILINE)
        match = pattern.search(json_string)
        if match:
            result = match.group(1).replace('\\"', '"').replace("\\\\", "\\").strip('"').strip("'").strip()
            # result = f"\"{result}\""
            return result
        raise ValueError(f"Could not find {key} in {json_string}")

    @staticmethod
    def _extract_response(
        chat_history: str,
        begin_marker: str = "[RESPONSE_BEGIN]",
        end_marker: str = "[RESPONSE_END]",
        ai_msg_marker: str = "AI:",
    ):
        code_blocks = chat_history.split(ai_msg_marker)
        pattern = r"\[RESPONSE_BEGIN\](.*?)\[RESPONSE_END\]"

        cleaned_output = []
        for code_block in code_blocks:
            matches = re.findall(pattern, code_block, re.DOTALL)
            if matches:
                cleaned_output.append(matches[0].strip())
        return "\n".join(cleaned_output)

    @classmethod
    def extract_action_for_llm(cls, text, max_token: int = 500) -> str:
        """Since Action should be fully inputted into an Agent, so we do not perform truncation here."""
        action_format = ACTION_FORMAT
        cleaned_output = text.strip()
        try:
            _action = cls._extract_value(cleaned_output, "action")
            _action_input = cls._extract_value(cleaned_output, "action_input")
            return action_format.format(_action=_action, _action_input=_action_input)
        except Exception:
            if cleaned_output.startswith("Action:"):
                lines = cleaned_output.splitlines()
                _action = lines[1].strip()
                _action_input = textwrap.dedent("\n".join(lines[2:])).strip()
                return action_format.format(_action=_action, _action_input=_action_input)
            else:
                _action_input = cleaned_output

            return action_format.format(_action="Final Answer", _action_input=_action_input)

    @classmethod
    def extract_tool_response_for_llm(cls, text, tool_style: str = "code", max_token: int = 250) -> str:
        wrap_format = TOOL_RESPONSE_FORMAT
        tool_observation_format = TOOL_FORMAT[tool_style]
        cleaned_output = text.strip()
        if tool_style == "plugin":
            max_token = None

        try:
            _result = cls.truncate_text(cls._extract_value(cleaned_output, "result"), max_token)
            _intermediate_steps = cls.truncate_text(
                cls._extract_value(cleaned_output, "intermediate_steps"), max_token
            )
            _intermediate_steps = _intermediate_steps.replace("\\n", "\n").strip("\n")
            _result = _result.replace("\\n", "\n").strip("\n")
            _response = tool_observation_format.format(_intermediate_steps=_intermediate_steps, _result=_result)

            return wrap_format.format(_response=_response)
        except:
            if cleaned_output.startswith("Final Answer:"):
                lines = cleaned_output.splitlines()
                _response = textwrap.dedent("\n".join(lines[2:])).strip()
                _response = cls.truncate_text(_response, max_token)
                return wrap_format.format(_response=_response)

            _response = cls.truncate_text(cleaned_output, max_token)
            return wrap_format.format(_response=_response)

    @classmethod
    def extract_code_for_python_tool(cls, text: str, max_token: int = 2500, trunc_ratio: float = 0.2) -> str:
        whole_code = MessageDataModel._extract_response(text)
        trunc_code = cls.truncate_text(whole_code, max_token=max_token, trunc_ratio=trunc_ratio)
        return trunc_code

    @classmethod
    def extract_code_for_sql_tool(cls, text: str, max_token: int = 2500, trunc_ratio: float = 0.2) -> str:
        whole_code = MessageDataModel._extract_response(text)
        trunc_code = cls.truncate_text(whole_code, max_token=max_token, trunc_ratio=trunc_ratio)
        return trunc_code
