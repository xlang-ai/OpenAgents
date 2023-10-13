from typing import Any, Dict, List, Optional, Tuple
from pydantic import root_validator

from langchain.memory.utils import get_prompt_input_key
from langchain.base_language import BaseLanguageModel
from langchain.schema import BaseMessage, get_buffer_string
from langchain.memory.chat_memory import BaseChatMemory, BaseMemory

from real_agents.adapters.data_model import DataModel, MessageDataModel


class ConversationBufferMemory(BaseChatMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:

    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        if self.return_messages:
            return self.chat_memory.messages
        else:
            return get_buffer_string(
                self.chat_memory.messages,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}


class ConversationStringBufferMemory(BaseMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    """Prefix to use for AI generated responses."""
    buffer: str = ""
    output_key: Optional[str] = None
    input_key: Optional[str] = None
    memory_key: str = "history"  #: :meta private:

    @root_validator()
    def validate_chains(cls, values: Dict) -> Dict:
        """Validate that return messages is not True."""
        if values.get("return_messages", False):
            raise ValueError("return_messages must be False for ConversationStringBufferMemory")
        return values

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.
        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        human = f"{self.human_prefix}: " + inputs[prompt_input_key]
        ai = f"{self.ai_prefix}: " + outputs[output_key]
        self.buffer += "\n" + "\n".join([human, ai])

    def clear(self) -> None:
        """Clear memory contents."""
        self.buffer = ""


class ConversationReActBufferMemory(BaseChatMemory):
    """Buffer for storing conversational ReAct memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:
    max_token_limit: int = 2000
    llm: BaseLanguageModel = None
    style: str = "code"

    @property
    def observation_prefix(self) -> str:
        """Prefix to append the observation with."""
        return "Observation: "

    @property
    def action_prefix(self) -> str:
        """Prefix to append the action with."""
        return "Action:"

    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return "Thought:"

    @property
    def llm_final(self) -> str:
        """Final Answer"""

    @property
    def buffer(self) -> List[BaseMessage]:
        """String buffer of memory."""
        if self.return_messages:
            return self.chat_memory.messages
        else:
            return get_buffer_string(
                self.chat_memory.messages,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    def _get_input_output(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> Tuple[str, str]:
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) == 1:
                output_key = list(outputs.keys())[0]
                return inputs[prompt_input_key], outputs[output_key]
            else:
                assert "intermediate_steps" in outputs, "intermediate_steps must in outputs when output_key length > 1"
                intermediate_message = ""
                for action, full_observation in outputs["intermediate_steps"]:
                    intermediate_message += "\n{\n"
                    intermediate_message += (
                        '\t"action": "{}"'.format(action.tool) + "\n"
                    )  # todo: move to schema, as well as the one in prompt
                    intermediate_message += '\t"action_input": "{}"'.format(action.tool_input) + "\n"
                    intermediate_message += "}\n"
                    observation = full_observation
                    if isinstance(full_observation, DataModel):
                        llm_raw_observation = full_observation.get_llm_side_data()
                        observation = MessageDataModel.extract_tool_response_for_llm(
                            llm_raw_observation, tool_style=self.style
                        )
                    intermediate_message += "{}\n".format(observation)
                output = intermediate_message + outputs[list(outputs.keys())[0]]

                return inputs[prompt_input_key], output
        else:
            output_key = self.output_key
        return inputs[prompt_input_key], outputs[output_key]

    def fit_max_token_limit(self):
        from real_agents.adapters.data_model import MessageDataModel

        # if self.llm != None:
        buffer = self.chat_memory.messages
        # curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
        curr_buffer_length = MessageDataModel._count_tokens("\n".join([_.content for _ in buffer]))
        if curr_buffer_length > self.max_token_limit:
            while curr_buffer_length > self.max_token_limit:
                buffer.pop(0)
                curr_buffer_length = MessageDataModel._count_tokens("\n".join([_.content for _ in buffer]))
                # curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
        self.chat_memory.messages = buffer

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer. Pruned."""
        super().save_context(inputs, outputs)
        self.fit_max_token_limit()
