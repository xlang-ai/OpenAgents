"""Chain for interacting with SQL Database."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Extra, Field
from loguru import logger

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain import BasePromptTemplate, FewShotPromptTemplate

from real_agents.data_agent.evaluation.sql_evaluator import SQLEvaluator
from real_agents.adapters.schema import SQLDatabase
from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.data_agent.sql.prompt import (
    EXAMPLE_PROMPT,
    FEW_SHOT_INPUT_VARIABLES,
    FEW_SHOT_PREFIX,
    FEW_SHOT_SUFFIX,
    PROMPT,
)
from real_agents.adapters.llm import LLMChain
from real_agents.adapters.data_model import MessageDataModel


class SQLDatabaseChain(Chain, BaseModel):
    """Chain for interacting with SQL Database"""

    llm: BaseLanguageModel
    """LLM wrapper to use."""
    database: SQLDatabase = Field(exclude=True)
    """SQL Database to connect to."""
    example_selector: Any = None
    """Example selector to select few-shot in-context exemplars."""
    memory: Optional[ReadOnlySharedStringMemory] = None
    """Shared memory."""
    prompt: BasePromptTemplate = PROMPT
    """Prompt to use to translate natural language to SQL."""
    input_key: str = "user_intent"  #: :meta private:
    output_key: str = "result"  #: :meta private:
    return_intermediate_steps: bool = False
    """Whether or not to return the intermediate steps along with the final answer."""
    return_direct: bool = False
    """Whether or not to return the result of querying the SQL table directly."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.
        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.
        :meta private:
        """
        if not self.return_intermediate_steps:
            return [self.output_key]
        else:
            # return [self.output_key, "intermediate_steps", "binder_steps"]
            return [self.output_key, "intermediate_steps"]

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        logger.bind(msg_head="SQLChain inputs").trace(inputs)

        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        if self.example_selector is not None:
            self.prompt = FewShotPromptTemplate(
                example_selector=self.example_selector,
                example_prompt=EXAMPLE_PROMPT,
                prefix=FEW_SHOT_PREFIX,
                suffix=FEW_SHOT_SUFFIX,
                input_variables=FEW_SHOT_INPUT_VARIABLES,
            )
        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        input_text = f"{inputs[self.input_key]} \nSQLQuery:"
        _run_manager.on_text(input_text, verbose=self.verbose)

        # If not present, then defaults to None which is all tables.
        table_names_to_use = inputs.get("table_names_to_use")
        table_info = self.database.get_table_info(table_names=table_names_to_use)
        llm_inputs = {
            "question": input_text,
            "dialect": self.database.dialect,
            "table_info": table_info,
            "chat_history": "",
            "stop": ["\nSQLResult:"],
        }

        # Load memory into chat history
        if self.memory is not None:
            llm_inputs["chat_history"] = self.memory.load_memory_variables({})["chat_history"]
            llm_inputs["chat_history"] = MessageDataModel.extract_code_for_sql_tool(llm_inputs["chat_history"])
        sql_cmd = llm_chain.predict(**llm_inputs)
        # TODO: Move this post-processing to a post-process function
        sql_cmd = sql_cmd.replace("\n", " ")
        if sql_cmd.endswith('"') and sql_cmd.startswith('"'):
            sql_cmd = sql_cmd.strip('"')
        if sql_cmd.endswith("'") and sql_cmd.startswith("'"):
            sql_cmd = sql_cmd.strip("'")

        logger.bind(msg_head="SQLChain generate program").trace(sql_cmd)

        # Call SQL/binder evaluator to execute the SQL command
        sql_evaluator = SQLEvaluator()
        result = sql_evaluator.run(sql_cmd, self.database)

        logger.bind(msg_head="SQLChain execution result").trace(result)

        # If return direct, we just set the final result equal to the sql query
        if self.return_direct:
            final_result = result
        else:
            input_text += f"{sql_cmd}\nSQLResult: {result}\nAnswer:"
            llm_inputs["input"] = input_text
            final_result = llm_chain.predict(**llm_inputs)
            _run_manager.on_text(final_result, color="green", verbose=self.verbose)
        chain_result: Dict[str, Any] = {self.output_key: final_result}
        if self.return_intermediate_steps:
            chain_result["intermediate_steps"] = sql_cmd
        return chain_result

    @property
    def _chain_type(self) -> str:
        return "sql_database_chain"
