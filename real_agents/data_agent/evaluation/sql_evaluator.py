import traceback
from typing import Any, Dict, List

from pydantic import root_validator

from real_agents.adapters.schema import SQLDatabase


class SQLEvaluator:
    """
    Util class for SQL code evaluation.
    """

    name = "SQL Evaluator"
    ERROR_PREFIX = "[ERROR]: "

    @root_validator(pre=True)
    def validate(cls, values: Dict) -> Any:
        """validate requirements for evaluation"""
        try:
            import sqlite3  # noqa F401 E402

            import sqlalchemy  # noqa F401 E402
        except ImportError:
            raise ValueError("This tool relies on sqlite3 and sqlalchemy, use `pip` to install these packages")
        return values

    @staticmethod
    def parse_command(program: str) -> List[str]:
        """patchify the code"""
        program_lines = program.strip().split("\n")
        return program_lines

    def run(self, program: str, environment: SQLDatabase) -> Any:
        """run generated code in certain environment"""
        try:
            output = environment.run(program)
            return {
                "success": True,
                "result": output,
            }
        except Exception as e:
            traceback.print_exc()
            error_message = str(e)
            return {"success": False, "error_message": f"{self.ERROR_PREFIX}{error_message}"}
