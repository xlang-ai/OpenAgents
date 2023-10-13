"""An agent designed to hold a conversation in addition to using tools. (Specially designed for plugins model)"""
from __future__ import annotations

from typing import Any, List, Optional, Sequence, Tuple, Union
from pydantic import Extra, Field
from typing_extensions import override

from langchain.agents.agent import AgentOutputParser
from langchain.agents.utils import validate_tools_single_input
from langchain.base_language import BaseLanguageModel
from langchain.chains import LLMChain
from langchain.schema import (
    AgentAction,
    AgentFinish,
    AIMessage,
    BaseMessage,
    BaseOutputParser,
    HumanMessage
)
from langchain.callbacks.manager import (
    Callbacks
)
from langchain.tools.base import BaseTool
from langchain.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from real_agents.adapters.agent_helpers.agent import Agent
from real_agents.adapters.agent_helpers.output_parser import ConversationOutputParser
from real_agents.plugins_agent.plugin_prompt import (
    PREFIX,
    SUFFIX,
    TEMPLATE_TOOL_RESPONSE,
    fake_continue_prompt
)
from real_agents.adapters.data_model import DataModel, MessageDataModel
from real_agents.data_agent.copilot import ConversationalChatAgent


class ConversationalPluginChatAgent(ConversationalChatAgent):
    """An agent designed to hold a conversation in addition to using plugin tool."""

    output_parser: ConversationOutputParser = Field(
        default_factory=ConversationOutputParser()
    )

    template_tool_response: str = TEMPLATE_TOOL_RESPONSE
    continue_model: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.allow
        arbitrary_types_allowed = True

    @classmethod
    def _get_default_output_parser(
            cls, **kwargs: Any
    ) -> ConversationOutputParser:
        return ConversationOutputParser()

    @property
    def _agent_type(self) -> str:
        raise NotImplementedError

    @property
    def observation_prefix(self) -> str:
        """Prefix to append the observation with."""
        return "Observation: "

    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return "Thought:"

    @classmethod
    def _validate_tools(cls, tools: Sequence[BaseTool]) -> None:
        super()._validate_tools(tools)
        validate_tools_single_input(cls.__name__, tools)

    @classmethod
    def create_prompt(
            cls,
            tools: Sequence[BaseTool],
            system_message: str = PREFIX,
            human_message: str = SUFFIX,
            input_variables: Optional[List[str]] = None,
            output_parser: Optional[BaseOutputParser] = None,
    ) -> BasePromptTemplate:
        tool_strings = "\n".join([f"Name: {tool.name}\nDescription: {tool.description}" for tool in tools])
        tool_strings = tool_strings.replace("{", "{{").replace("}", "}}")
        tool_names = ", ".join([tool.name for tool in tools])
        _output_parser = output_parser or cls._get_default_output_parser()

        format_instructions = _output_parser.get_format_instructions("plugins")
        format_instructions = format_instructions.format(tool_names=tool_names)

        # system message
        system_message = system_message + f"{tool_strings}\n\n{format_instructions}"

        # human input
        final_prompt = human_message

        if input_variables is None:
            input_variables = ["input", "chat_history", "agent_scratchpad"]
        messages = [
            SystemMessagePromptTemplate.from_template(system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(final_prompt),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    def _construct_scratchpad(self, intermediate_steps: List[Tuple[AgentAction, str]]) -> List[BaseMessage]:
        """Construct the scratchpad that lets the agent continue its thought process."""
        thoughts: List[BaseMessage] = []
        # Try to only use AI message for scratchpad
        content = []
        for idx, (action, full_observation) in enumerate(intermediate_steps):
            content.append(MessageDataModel.extract_action_for_llm(action.log))

            observation = full_observation
            if isinstance(full_observation, DataModel):
                llm_raw_observation = full_observation.get_llm_side_data()

                observation = MessageDataModel.extract_tool_response_for_llm(llm_raw_observation, tool_style="plugin")
                tool_response = self.template_tool_response.format(
                    observation=str(observation), tool_names=self.allowed_tools
                )
                if idx == len(intermediate_steps) - 1:
                    content.append(tool_response)
                else:
                    content.append(observation)

        content_str = "\n".join(content)
        thoughts.append(AIMessage(content=content_str))
        if self.continue_model is not None and len(intermediate_steps) != 0:
            thoughts.append(HumanMessage(content=fake_continue_prompt[self.continue_model]))
        return thoughts

    @override
    def plan(
            self,
            intermediate_steps: List[Tuple[AgentAction, str]],
            **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        full_inputs = self.get_full_inputs(intermediate_steps, **kwargs)
        system_prompt = self.llm_chain.prompt.messages[0].format().content
        system_prompt_tokens = MessageDataModel._count_tokens(
            system_prompt
        )
        max_tokens = 8000
        max_gen_tokens = 1000
        # FIXME: need more accurate token limit calculation
        full_inputs = MessageDataModel.truncate_chat_history(full_inputs,
                                                             max_token=max_tokens - system_prompt_tokens - max_gen_tokens)
        full_output = self.llm_chain.predict(**full_inputs)

        return self.output_parser.parse(full_output)

    @classmethod
    def from_llm_and_tools(
            cls,
            llm: BaseLanguageModel,
            tools: Sequence[BaseTool],
            callbacks: Callbacks = None,
            output_parser: Optional[AgentOutputParser] = None,
            system_message: str = PREFIX,
            human_message: str = SUFFIX,
            input_variables: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> Agent:
        """Construct an agent from an LLM and tools."""
        cls._validate_tools(tools)

        _output_parser = output_parser or cls._get_default_output_parser()
        prompt = cls.create_prompt(
            tools,
            system_message=system_message,
            human_message=human_message,
            input_variables=input_variables,
            output_parser=_output_parser,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
        )
        tool_names = [tool.name for tool in tools]
        return cls(
            llm_chain=llm_chain,
            allowed_tools=tool_names,
            output_parser=_output_parser,
            **kwargs,
        )
