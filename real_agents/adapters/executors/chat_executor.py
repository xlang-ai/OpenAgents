from typing import Any, Dict

from langchain.base_language import BaseLanguageModel
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.chains import ConversationChain

from real_agents.adapters.executors.base import BaseExecutor
from real_agents.adapters.memory import ConversationBufferMemory


class ChatExecutor(BaseExecutor):
    """Chat Executor."""

    _DEFAULT_TEMPLATE = "The following is a friendly conversation between a human and an AI. \
        The AI is talkative and provides lots of specific details from its context. \
        If the AI does not know the answer to a question, it truthfully says it does not know."
    output_key: str = "result"

    def __init__(self) -> None:
        """Initialize the executor"""
        self.memory = ConversationBufferMemory(return_messages=True)

    def run(
        self,
        user_intent: str,
        llm: BaseLanguageModel,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Run the executor.

        Args:
            user_intent: User intent to execute.
            grounding_source: Grounding source to execute the program on.
            llm: Language model to use.
            verbose: Whether to print the logging.

        Returns:
            Result of string.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self._DEFAULT_TEMPLATE),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )
        method = ConversationChain(
            llm=llm,
            prompt=prompt,
            verbose=verbose,
            memory=self.memory,
        )
        result = method.predict(input=user_intent)
        output = {self.output_key: result}
        return output
