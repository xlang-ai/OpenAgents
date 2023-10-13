from __future__ import annotations

from typing import Any, Optional, Sequence

from langchain.base_language import BaseLanguageModel
from langchain.tools.base import BaseTool

from real_agents.adapters.agent_helpers import AgentExecutor
from real_agents.data_agent.copilot import ConversationalChatAgent
from real_agents.plugins_agent.plugin import ConversationalPluginChatAgent
from real_agents.web_agent.webot import ConversationalWebotChatAgent


def initialize_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    continue_model: str = None,
    agent_kwargs: Optional[dict] = None,
    return_intermediate_steps: Optional[bool] = True,
    **kwargs: Any,
) -> AgentExecutor:
    """Load an agent executor given tools and LLM.

    Args:
        tools: List of tools this agent has access to.
        llm: Language model to use as the agent.
        callback_manager: CallbackManager to use. Global callback manager is used if
            not provided. Defaults to None.
        agent_kwargs: Additional key word arguments to pass to the underlying agent_executor
        return_intermediate_steps: Whether to return intermediate steps in the agent
        **kwargs: Additional key word arguments passed to the agent executor

    Returns:
        An agent executor
    """

    agent_kwargs = agent_kwargs or {}
    agent_obj = ConversationalChatAgent.from_llm_and_tools(
        llm=llm, tools=tools, continue_model=continue_model, **agent_kwargs
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        return_intermediate_steps=return_intermediate_steps,
        **kwargs,
    )
    return agent_executor


def initialize_plugin_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    continue_model: str = None,
    agent_kwargs: Optional[dict] = None,
    return_intermediate_steps: Optional[bool] = True,
    **kwargs: Any,
) -> AgentExecutor:
    """Load an agent executor given tools and LLM.

    Args:
        tools: List of tools this agent has access to.
        llm: Language model to use as the agent.
        agent_kwargs: Additional key word arguments to pass to the underlying agent_executor
        return_intermediate_steps: Whether to return intermediate steps in the agent
        **kwargs: Additional key word arguments passed to the agent executor

    Returns:
        An agent executor
    """

    agent_kwargs = agent_kwargs or {}
    agent_obj = ConversationalPluginChatAgent.from_llm_and_tools(
        llm=llm, tools=tools, continue_model=continue_model, **agent_kwargs
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        return_intermediate_steps=return_intermediate_steps,
        **kwargs,
    )
    return agent_executor


def initialize_webot_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    continue_model: str = None,
    agent_kwargs: Optional[dict] = None,
    return_intermediate_steps: Optional[bool] = True,
    **kwargs: Any,
) -> AgentExecutor:
    """Load an agent executor given tools and LLM.

    Args:
        tools: List of tools this agent has access to.
        llm: Language model to use as the agent.
        agent_kwargs: Additional key word arguments to pass to the underlying agent_executor
        return_intermediate_steps: Whether to return intermediate steps in the agent
        **kwargs: Additional key word arguments passed to the agent executor

    Returns:
        An agent executor
    """

    agent_kwargs = agent_kwargs or {}
    agent_obj = ConversationalWebotChatAgent.from_llm_and_tools(
        llm=llm, tools=tools, continue_model=continue_model, **agent_kwargs
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        return_intermediate_steps=return_intermediate_steps,
        **kwargs,
    )
    return agent_executor
