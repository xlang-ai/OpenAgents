from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Extra

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain

from real_agents.adapters.executors.question_suggestion.prompts import QUESTION_SUGGESTION_PROMPT_BASE


class QuestionSuggestionChainBase(Chain, BaseModel):
    """Question Suggestion by Language Models."""

    llm_chain: LLMChain
    output_key: str = "questions"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.

        :meta private:
        """
        return self.llm_chain.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.

        :meta private:
        """
        return [self.output_key]

    def extract_questions(self, s: str) -> List[str]:
        components = s.split("\n")
        questions = []
        count = 1
        for c in components:
            if c.startswith(f"{count}"):
                questions.append(c.replace(f"{count}.", "").replace(f"{count}", "").strip())
                count += 1
        return questions

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, List[str]]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        questions = self.llm_chain.predict(**inputs)
        _run_manager.on_text(questions, color="green", end="\n", verbose=False)
        return {self.output_keys[0]: self.extract_questions(questions)}

    @classmethod
    def from_prompt(cls, llm: BaseLanguageModel) -> QuestionSuggestionChainBase:
        """Load from base prompt."""
        llm_chain = LLMChain(llm=llm, prompt=QUESTION_SUGGESTION_PROMPT_BASE)
        return cls(llm_chain=llm_chain)
