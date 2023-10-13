from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from real_agents.adapters.data_model.base import DataModel
from real_agents.adapters.data_model.templates.skg_templates.database_templates import serialize_db
from real_agents.adapters.data_model.templates.skg_templates.table_templates import serialize_df
import json


class KaggleDataModel(DataModel):
    """A data model for KaggleDataModel.
    We only support the csv and sqlite format for now.
    raw_data is a Dict[str, TableDataModel]
    raw_data_path is List[str]
    raw_data_name is Dict[str, str]
    """

    def get_llm_side_data(self, serialize_method: str = "tsv", num_visible_rows: int = 3) -> Any:
        formatted_tables = []
        for _raw_data_path in self.raw_data_path:
            table_data = self.raw_data[_raw_data_path]
            table_name = self.raw_data_name[_raw_data_path]
            table_path = _raw_data_path
            formatted_table = serialize_df(table_data, table_name, table_path, serialize_method, num_visible_rows)
            formatted_tables.append(formatted_table)
        return "\n".join(formatted_tables)

    @staticmethod
    def to_react_table(table: pd.DataFrame) -> str:
        columns = list(map(lambda item: {"accessorKey": item, "header": item}, table.columns.tolist()))
        # FIXME: NaN may not be handled here.
        data = table.fillna("").to_dict(orient="records")
        table = json.dumps({"columns": columns, "data": data})
        return table

    def get_human_side_data(self) -> Any:
        # In the frontend, we show the first few rows of each table
        react_tables = {}
        for table_path in self.raw_data_path:
            table_name = self.raw_data_name[table_path]
            table = self.raw_data[table_path]
            react_tables[table_name] = self.to_react_table(table)
        return json.dumps(react_tables)
