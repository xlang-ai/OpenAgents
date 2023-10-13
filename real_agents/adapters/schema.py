from typing import NamedTuple
from langchain import SQLDatabase
from sqlalchemy import text
from sqlalchemy.engine import Row
from tabulate import tabulate
from typing import List, Any


class AgentTransition(NamedTuple):
    """Agent's transition to take."""

    return_values: dict
    log: str


EMPTY_RESULT_STR = "NONE"  # to show NONE result in front-end.


class SQLDatabase(SQLDatabase):
    @staticmethod
    def _pretty_format(headers: Any, result: List[Row]) -> str:
        dicts = [dict(zip(headers, row)) for row in result]
        tab_result = tabulate(tabular_data=dicts, headers="keys", tablefmt="psql")

        if tab_result == "":
            return EMPTY_RESULT_STR

        return tab_result

    def run(self, command: str, fetch: str = "all") -> str:
        """Execute a SQL command and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        with self._engine.begin() as connection:
            if self._schema is not None:
                connection.exec_driver_sql(f"SET search_path TO {self._schema}")
            cursor = connection.execute(text(command))
            if cursor.returns_rows:
                headers = cursor.keys()
                if fetch == "all":
                    result = cursor.fetchall()
                elif fetch == "one":
                    # result = cursor.fetchone()[0]  # type: ignore
                    result = [cursor.fetchone()]  # type: ignore
                else:
                    raise ValueError("Fetch parameter must be either 'one' or 'all'")

                # pretty format
                tab_result = self._pretty_format(headers, result)
                return tab_result
        return ""
