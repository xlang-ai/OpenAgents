"""Callback Handler streams to stdout on new llm token."""
from typing import Any, Dict, List, Union

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from real_agents.adapters.data_model import DataModel


class JSON_PDA:
    def __init__(self):
        self.stack = []
        self.state = "start"
        self.json = {}
        self.current_key = ""
        self.current_value = ""
        self.escape_next = False

    def transition(self, char):
        if self.escape_next:
            # Add the escaped character to the current key or value and return
            if self.state == "open_key_quote":
                self.current_key += char
            elif self.state == "open_value_quote" or self.state == "open_value_quote_brace":
                self.current_value += char
            self.escape_next = False
            return

        if char == "\\":
            # The next character is an escaped character
            self.escape_next = True
            return

        if self.state == "start":
            if char == "{":
                self.stack.append("{")
                self.state = "open_brace"
            elif char == "`":
                self.state = "open_one_backtick"
                self.stack.append("`")
        elif self.state == "open_one_backtick":
            if char == "`":
                if self.stack[-1] == "`":
                    self.state = "open_two_backticks"
                    self.stack.append("`")
                else:
                    while self.stack.pop() != "`":
                        pass
                    self.state = "start"
            else:
                self.stack.append(char)
        elif self.state == "open_two_backticks":
            if char == "`":
                if self.stack[-1] == "`":
                    self.state = "after_backtick"
                    self.stack.append("`")
                else:
                    while self.stack.pop() != "`":
                        pass
                    self.state = "start"
            else:
                self.stack.append(char)
        elif self.state == "after_backtick":
            if char == "\n":
                self.state = "after_backtick_newline"
        elif self.state == "after_backtick_newline":
            if char == "{":
                self.stack.append("{")
                self.state = "open_brace"
            elif char == "\n":
                self.state = "after_backtick_newline"
            else:
                self.state = "in_block"
        elif self.state == "in_block":
            if char == "`":
                self.stack.pop()
                if len(self.stack) == 0:
                    self.state = "start"
        elif self.state == "open_brace" or self.state == "comma":
            if char == '"':
                self.stack.append('"')
                self.state = "open_key_quote"
                self.current_key = ""
        elif self.state == "open_key_quote" or self.state == "open_value_quote":
            if char != '"':
                if self.state == "open_key_quote":
                    self.current_key += char
                else:
                    self.current_value += char
            else:
                self.stack.pop()
                if self.state == "open_key_quote":
                    self.state = "close_key_quote"
                else:
                    self.state = "close_value_quote"
        elif self.state == "open_value_quote_brace":
            if char == "{":
                self.stack.append("{")
            elif char == "}":
                self.stack.pop()
                if self.stack[-1] == "{" and self.stack[-2] != "{":
                    self.state = "close_value_quote"
            self.current_value += char
        elif self.state == "close_key_quote":
            if char == ":":
                self.state = "after_key"
        elif self.state == "after_key":
            if char == '"':
                self.stack.append('"')
                self.state = "open_value_quote"
                self.current_value = ""
            elif char == "{":
                self.stack.append("{")
                self.state = "open_value_quote_brace"
                self.current_value = "{"
        elif self.state == "close_value_quote":
            self.json[self.current_key] = self.current_value
            if char == ",":
                self.state = "after_value"
            elif char == "}":
                self.stack.pop()
                if len(self.stack) == 0:
                    self.state = "start"
                elif len(self.stack) == 3:
                    self.state = "close_brace"
        elif self.state == "after_value":
            if char == '"':
                self.stack.append('"')
                self.state = "open_key_quote"
        elif self.state == "close_brace":
            if char == "`":
                self.stack.pop()
                if len(self.stack) == 0:
                    self.state = "start"


class AgentStreamingStdOutCallbackHandler(StreamingStdOutCallbackHandler):
    is_end = False
    generated_tokens: list = []
    for_display: list = []

    # Automata
    pda = JSON_PDA()
    llm_call_id = 0
    _in_json = False
    _in_key = False
    _in_value = False
    _direct_display = True
    _normal_json = False
    json_key: str = ""
    json_tmp_stack: list = []
    action_key_appear = False

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.is_end = False
        self.generated_tokens = []

        self.pda = JSON_PDA()
        self.llm_call_id += 1
        self._in_json = False
        self._in_key = False
        self._in_value = False
        self._direct_display = True
        self._normal_json = False
        self.json_key = ""
        self.json_tmp_stack = []

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """
        Run on new LLM token. Only available when streaming is enabled.
        The tokens that we can decide their types ('plain', 'identifier', 'key', 'action', 'action_input') are stored in `self.for_display`.
        """
        self.generated_tokens.append(token)

        # Automata that monitor json block
        for char in token:
            self.pda.transition(char)

            # Handle the logic of sentences and json blocks
            _type = "plain"

            if self.pda.state in ["open_brace", "open_one_backtick"]:
                self._in_json = True
                self._direct_display = False
                self._normal_json = False
                self.action_key_appear = False

            if self._in_json and not self._normal_json:
                _type = "identifier"

                if self.pda.state == "in_block":
                    _type = "plain"
                    self._normal_json = True

                if self.pda.state == "open_key_quote":
                    if self._in_key:
                        self.json_key += char
                        _type = "key"
                    self._in_key = True
                else:
                    self._in_key = False

                if self.pda.state == "open_value_quote" or self.pda.state == "open_value_quote_brace":
                    if self._in_value:
                        _type = self.json_key
                    self._in_value = True
                else:
                    if self._in_value:
                        self.json_key = ""
                    self._in_value = False

                if self.pda.state == "close_key_quote":
                    # Normal json block

                    if self.json_key not in ["action", "action_input"]:
                        for char_item in self.json_tmp_stack:
                            self.for_display.append(
                                {"text": char_item["text"], "type": "plain", "llm_call_id": self.llm_call_id}
                            )
                        self.json_tmp_stack = []
                        self.for_display.append({"text": char, "type": "plain", "llm_call_id": self.llm_call_id})
                        self._normal_json = True
                        continue

                    else:
                        if self.json_key == "action":
                            self.action_key_appear = True

                        elif self.json_key == "action_input" and self.action_key_appear:
                            # Action json block
                            for char_item in self.json_tmp_stack:
                                char_item["llm_call_id"] = self.llm_call_id
                                self.for_display.append(char_item)
                            self.json_tmp_stack = []
                            self._direct_display = True

            else:
                for char_item in self.json_tmp_stack:
                    self.for_display.append(
                        {"text": char_item["text"], "type": "plain", "llm_call_id": self.llm_call_id}
                    )
                self.json_tmp_stack = []
                self._direct_display = True

            if self.pda.state == "start":
                self._in_json = False

            self.for_display.append(
                {"text": char, "type": _type, "llm_call_id": self.llm_call_id}
            ) if self._direct_display else self.json_tmp_stack.append(
                {"text": char, "type": _type, "llm_call_id": self.llm_call_id}
            )

    def on_llm_end(self, response, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.is_end = True
        for char_item in self.json_tmp_stack:
            self.for_display.append({"text": char_item["text"], "type": "plain", "llm_call_id": self.llm_call_id})

    def on_tool_end(self, output: Union[DataModel, str], **kwargs: Any) -> None:
        """Run on tool end to add observation data model."""
        self.for_display.append({"text": output, "type": "block", "llm_call_id": self.llm_call_id})
