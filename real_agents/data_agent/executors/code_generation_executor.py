from typing import Any, Dict, List, Literal, Optional, Union

from langchain.base_language import BaseLanguageModel

from real_agents.adapters.data_model import DatabaseDataModel, TableDataModel, ImageDataModel
from real_agents.adapters.memory import ReadOnlySharedStringMemory
from real_agents.adapters.schema import SQLDatabase
from real_agents.data_agent.python.base import PythonChain
from real_agents.data_agent.sql.base import SQLDatabaseChain


class CodeGenerationExecutor:
    """Code Generation Executor.

    Example:
        .. code-block:: python

                from real_agents.adapters.executors import CodeGenerationExecutor
                executor = CodeGenerationExecutor(programming_language="sql")
                executor.run(
                    user_intent="What is the name of the first employee?",
                    grounding_source=SQLDatabase.from_uri(...)
                )

    """

    def __init__(
        self,
        programming_language: Literal["sql", "python"],
        usage: Union[None, str] = None,
        example_selector: Any = None,
        memory: Optional[ReadOnlySharedStringMemory] = None,
    ) -> None:
        """Initialize the executor.

        Args:
            programming_language: Programming language to generate.
            example_selector: Example selector to select few-shot in-context exemplars.
        """
        self._programming_language = programming_language
        self._usage = usage
        self._example_selector = example_selector
        self._memory = memory

    @property
    def programming_language(self) -> str:
        """Get programming language."""
        return self._programming_language

    def run(
        self,
        user_intent: str,
        llm: BaseLanguageModel,
        grounding_source: Optional[Union[List[TableDataModel], DatabaseDataModel, ImageDataModel]] = None,
        user_id: str = None,
        chat_id: str = None,
        code_execution_mode: str = "local",
        jupyter_kernel_pool: Any = None,
        return_intermediate_steps: bool = True,
        return_direct: bool = True,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """Run the executor.

        Args:
            user_intent: User intent to execute.
            grounding_source: Grounding source to execute the program on. should be {file_name: data}
            llm: Language model to use.
            return_intermediate_steps: Whether to return the intermediate steps, e.g., the program.
            return_direct: Whether to return the result of program execution directly.
            verbose: Whether to print the logging.

        Returns:
            Result dictionary of code generation
        """

        def _concat_grounding_source() -> str:
            assert isinstance(grounding_source, list)
            table_schema = ""
            for gs in grounding_source:
                table_schema += f"{gs.get_llm_side_data()}\n"
            return table_schema

        if self._programming_language == "sql":
            db = grounding_source.raw_data
            assert isinstance(db, SQLDatabase)
            method = SQLDatabaseChain(
                llm=llm,
                database=db,
                example_selector=self._example_selector,
                memory=self._memory,
                return_direct=return_direct,
                return_intermediate_steps=return_intermediate_steps,
                verbose=verbose,
            )
            _input = {"user_intent": user_intent}
            result = method(_input)
        elif self._programming_language == "python":
            if self._usage is None:
                # General python code generation for data analysis
                method = PythonChain.from_python_prompt(
                    llm,
                    return_intermediate_steps=return_intermediate_steps,
                    verbose=True,
                    memory=self._memory,
                    user_id=user_id,
                    chat_id=chat_id,
                    code_execution_mode=code_execution_mode,
                    jupyter_kernel_pool=jupyter_kernel_pool,
                )
                # Get each source_item (table, db, files...) from the grounding_source
                _input = {"question": user_intent, "data_info": _concat_grounding_source()}
                result = method(_input)
            elif self._usage == "echarts":
                # Python code generation for echarts interactive chart
                method = PythonChain.from_echarts_prompt(
                    llm,
                    return_intermediate_steps=return_intermediate_steps,
                    verbose=True,
                    memory=self._memory,
                    user_id=user_id,
                    chat_id=chat_id,
                    code_execution_mode=code_execution_mode,
                    jupyter_kernel_pool=jupyter_kernel_pool,
                )
                _input = {"question": user_intent, "data_info": _concat_grounding_source()}
                result = method(_input)
            else:
                raise ValueError(f"Usage {self._usage} not supported yet.")
        else:
            raise ValueError(f"Programming language {self._programming_language} not supported.")
        return result
