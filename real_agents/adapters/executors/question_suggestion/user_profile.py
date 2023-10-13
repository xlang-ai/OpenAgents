from __future__ import annotations

from langchain.base_language import BaseLanguageModel
from langchain.chains.llm import LLMChain

from real_agents.adapters.executors.question_suggestion.base import QuestionSuggestionChainBase
from real_agents.adapters.executors.question_suggestion.prompts import QUESTION_SUGGESTION_PROMPT_USER_PROFILE


class QuestionSuggestionChainUserProfile(QuestionSuggestionChainBase):
    @classmethod
    def from_prompt(cls, llm: BaseLanguageModel) -> QuestionSuggestionChainUserProfile:
        """Load from user profile prompt."""
        llm_chain = LLMChain(llm=llm, prompt=QUESTION_SUGGESTION_PROMPT_USER_PROFILE)
        return cls(llm_chain=llm_chain)
