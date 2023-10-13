"""Implements Python Code Generation. """
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from loguru import logger
from pydantic import BaseModel, Extra

from real_agents.adapters.data_model import MessageDataModel
from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.data_agent.evaluation.python_evaluator import PythonEvaluator
from real_agents.data_agent.python.echarts_prompt import E_SYSTEM_PROMPT, ECHARTS_REF_CODE, ECHARTS_USER_PROMPT
from real_agents.data_agent.python.system_prompt import SYSTEM_PROMPT
from real_agents.data_agent.python.python_prompt import USER_PROMPT
from real_agents.adapters.llm import LLMChain


class PythonChain(Chain, BaseModel):
    """Chain for Generating Python Code"""

    llm_chain: LLMChain

    memory: Optional[ReadOnlySharedStringMemory] = None
    stop: str = "\n\n"
    get_answer_expr: str = ""
    python_globals: Optional[Dict[str, Any]] = None
    python_locals: Optional[Dict[str, Any]] = None
    output_key: str = "result"  #: :meta private:
    return_intermediate_steps: bool = False
    code_execution_mode: str = "local"
    jupyter_kernel_pool: Optional[Any] = None
    reference_code: str = ""

    chat_id: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.ignore
        arbitrary_types_allowed = True

    def _validate_inputs(self, inputs: Dict[str, str]) -> None:
        """Check that all inputs are present."""
        missing_keys = set(self.input_keys).difference(inputs)
        if "chat_history" in missing_keys:
            missing_keys.remove("chat_history")
        if missing_keys:
            raise ValueError(f"Missing some input keys: {missing_keys}")

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.

        :meta private:
        """
        return ["data_info", "question", "chat_history"]

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.

        :meta private:
        """
        if not self.return_intermediate_steps:
            return [self.output_key]
        else:
            return [self.output_key, "intermediate_steps"]

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        logger.bind(msg_head="PythonChain inputs").trace(inputs)

        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        _run_manager.on_text(inputs[self.input_keys[0]])
        inputs["chat_history"] = ""
        if self.memory is not None:
            inputs["chat_history"] = self.memory.load_memory_variables({})["chat_history"]
            inputs["chat_history"] = MessageDataModel.extract_code_for_python_tool(inputs["chat_history"])

        history = {
            "history_code": inputs["chat_history"],
            "question": inputs["question"],
            "data": inputs["data_info"],
            "reference_code": self.reference_code,
        }

        # we apply llm as a magic function, which serves as python code generation func.
        raw_output = self.llm_chain.run(**history)

        def _extract_code(_raw_output: str) -> str:
            # Using 'html.parser' to parse the content
            soup = BeautifulSoup(_raw_output, "html.parser")
            try:
                _raw_output = soup.find("code").text
            except:
                pass
            if "```python:" in _raw_output:
                pattern = r"```python\n{(.*?)}\n```"
                match = re.search(pattern, _raw_output, re.DOTALL)
                if match:
                    return match.group(1)
                else:
                    return _raw_output
            else:
                return _raw_output

        code = _extract_code(raw_output).replace("\\n", "\n")

        logger.bind(msg_head="PythonChain generated program").trace(code)

        repl = PythonEvaluator(
            code_execution_mode=self.code_execution_mode,
            jupyter_kernel_pool=self.jupyter_kernel_pool,
        )

        """
        Since there will be error if we try to launch matplotlib GUI in the server,
        I add this line to avoid backend execution of matplotlib for now.
        """
        result = repl.run(code + f"\n{self.get_answer_expr}", user_id=self.user_id, chat_id=self.chat_id)

        logger.bind(msg_head="PythonChain execution result").trace(result)

        output = {self.output_key: result}
        if self.return_intermediate_steps:
            output["intermediate_steps"] = code
        return output

    @classmethod
    def create_python_prompt(cls, system_prompt: str, reference_code_prompt: str) -> BasePromptTemplate:
        input_variables = ["history_code", "question", "data", "reference_code"]
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(template=USER_PROMPT),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def create_echarts_prompt(cls, system_prompt: str, reference_code_prompt: str) -> BasePromptTemplate:
        input_variables = ["history_code", "question", "data", "reference_code"]
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(template=ECHARTS_USER_PROMPT),
        ]

        return ChatPromptTemplate(input_variables=input_variables, messages=messages)

    @classmethod
    def from_python_prompt(cls, llm: BaseLanguageModel, **kwargs: Any) -> PythonChain:
        """Load from Echarts prompt."""
        llm_chain = LLMChain(llm=llm, prompt=cls.create_python_prompt(SYSTEM_PROMPT, ""))
        return cls(
            llm_chain=llm_chain,
            get_answer_expr="",
            reference_code="",
            **kwargs,
        )

    @classmethod
    def from_echarts_prompt(cls, llm: BaseLanguageModel, **kwargs: Any) -> PythonChain:
        """Load from Echarts prompt."""
        llm_chain = LLMChain(llm=llm, prompt=cls.create_echarts_prompt(E_SYSTEM_PROMPT, ""))
        return cls(
            llm_chain=llm_chain,
            get_answer_expr="",
            reference_code=ECHARTS_REF_CODE,
            **kwargs,
        )

    @property
    def _chain_type(self) -> str:
        return "program_chain"
