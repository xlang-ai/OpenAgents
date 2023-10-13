from typing import Dict, Optional, List
import json
import base64
import re
import ast

import mo_sql_parsing
from pydantic import BaseModel

from real_agents.adapters.data_model import MessageDataModel, DataModel


def is_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def split_text_and_code(text: str) -> List:
    pattern = r"(```[\s\S]+?```)"
    result = [x for x in re.split(pattern, text) if x.strip()]

    return result


def detect_code_type(code) -> str:
    # Attempt Python parsing
    try:
        ast.parse(code)
        return "python"
    except SyntaxError:
        pass

    # Attempt SQL parsing
    try:
        mo_sql_parsing.parse(code)
        return "sql"
    except:
        pass

    # If all else fails, it's probably plain text
    return "text"


def add_backticks(text: str) -> str:
    """Add backticks to code blocks."""
    text_type = detect_code_type(text)
    if is_json(text):
        text = "```json\n" + text + "\n```"
    elif text_type == "python":
        if not text.startswith("```") and not text.endswith("```"):
            text = "```python\n" + text + "\n```"
    elif text_type == "sql":
        if not text.startswith("```") and not text.endswith("```"):
            text = "```sql\n" + text + "\n```"
    return text


class DisplayStream(BaseModel):
    """The display stream to parse and render tokens and blocks"""

    streaming_mode: str = "plain"
    action: str = ""
    action_cache: str = ""
    execution_result_max_tokens: int = 1000
    escape: bool = False
    escape_cache: str = ""
    llm_call_id: int = -1

    def reset(self):
        self.streaming_mode = "plain"
        self.action = ""
        self.action_cache = ""
        self.escape = False
        self.escape_cache = ""

    def display(self, token: Dict) -> Optional[List[Dict]]:
        # Reset if the llm_call_id has changed
        if token["llm_call_id"] != self.llm_call_id:
            self.llm_call_id = token["llm_call_id"]
            self.reset()
        # Handle escape characters
        import codecs

        if token["text"] == "\\":
            self.escape = True
            self.escape_cache = "\\"
            return None
        else:
            if self.escape:
                try:
                    token["text"] = codecs.decode(self.escape_cache + token["text"], "unicode_escape")
                    self.escape = False
                    self.escape_cache = ""
                except Exception as e:
                    self.escape_cache += token["text"]
        # Tool selection
        if self.action != "" and token["type"] != "action":
            # An action has been generated
            if self.action != "Final Answer":
                _pretty_name = self.action
                self.action_cache = self.action
                self.action = ""
                return [{"text": _pretty_name, "type": "tool", "final": False}]
        if token["type"] == "plain":
            # Display plain text
            if self.streaming_mode == "identifier":
                return None
            else:
                self.streaming_mode = "plain"
                return [{"text": token["text"], "type": "transition", "final": False}]
        elif token["type"] == "identifier":
            self.streaming_mode = "identifier"
            return None
        elif token["type"] == "key":
            self.streaming_mode = "key"
            return None
        elif token["type"] == "action":
            self.streaming_mode = "action"
            self.action += token["text"]
            return None
        elif token["type"] == "action_input":
            self.streaming_mode = "action_input"
            if self.action == "Final Answer":
                return [{"text": token["text"], "type": "plain", "final": True}]
        elif token["type"] == "block":
            observation = token["text"]
            result = self._display_observation(observation=observation)
            return result
        else:
            raise ValueError("Unknown token type: {}".format(token["type"]))

    def _display_observation(self, observation: Dict) -> Optional[List]:
        """Display the observation, i.e., the response from the tool

        Args:
            observation: Tool response block

        Returns:
            A list of display blocks to the frontend
        """
        tool_response_list = []
        if isinstance(observation, str):
            # Observation is a plain text (not used)
            tool_response_list.append({"text": observation, "type": "plain", "final": False})
            return tool_response_list

        assert isinstance(observation, DataModel), "Observation must be a DataModel object"
        observation = observation.get_human_side_data()

        assert isinstance(observation, Dict), "Observation must be a Dict object"

        result = observation.get("result", "")
        result_str = str(result)
        # Code & Plugin block
        if "intermediate_steps" in observation:
            intermediate_steps = observation["intermediate_steps"]
            if self.action_cache == "PythonCodeBuilder":
                intermediate_steps = "```python\n" + intermediate_steps + "\n```"
            elif self.action_cache == "SQLCodeBuilder":
                intermediate_steps = "```sql\n" + intermediate_steps + "\n```"
            else:
                intermediate_steps = add_backticks(intermediate_steps)
            tool_response_list.append({"text": intermediate_steps, "type": "plain", "final": False})

        # Execution result
        if not observation["success"]:
            tool_response_list.append({"text": result_str, "type": "error", "final": False})
        else:
            result_str = MessageDataModel.truncate_text(result_str, max_token=self.execution_result_max_tokens)

            tool_response_list.append(
                {
                    "text": f"""```console\n{result_str.strip(' ').strip("```")}\n```"""
                    if result_str.strip("```")
                    else "",
                    "type": "execution_result",
                    "final": False,
                }
            )
        # Kaggle search and connect
        if "kaggle_action" in observation:
            kaggle_action = observation["kaggle_action"]
            tool_response_list.append(
                {
                    "text": json.dumps(observation["kaggle_output_info"]),
                    "type": f"kaggle_{kaggle_action}",
                    "final": False,
                }
            )
        # Image result, e.g., matplotlib
        if "images" in observation:
            try:
                for image in observation["images"]:
                    if isinstance(image, str):
                        continue
                    image_data_64 = "data:image/png;base64," + base64.b64encode(
                        base64.b64decode(image.data["image/png"])
                    ).decode("utf-8")
                    tool_response_list.append({"text": image_data_64, "type": "image", "final": False})
            except:
                tool_response_list.append(
                    {"text": "[ERROR]: error rendering image/png", "type": "error", "final": False}
                )
        # Echarts
        if "echarts" in observation:
            chart_json = observation["echarts"]

            if is_json(chart_json):
                tool_response_list.append({"text": chart_json, "type": "echarts", "final": False})
            else:
                tool_response_list.append({"text": f"""```json{chart_json}```""", "type": "plain", "final": False})

        return tool_response_list
