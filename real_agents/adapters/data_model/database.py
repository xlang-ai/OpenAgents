from __future__ import annotations

import os
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, inspect

from real_agents.adapters.data_model.base import DataModel
from real_agents.adapters.data_model.table import TableDataModel
from real_agents.adapters.data_model.templates.skg_templates.database_templates import serialize_db
from real_agents.adapters.schema import SQLDatabase


class DatabaseDataModel(DataModel):
    """A data model for database."""

    @classmethod
    def from_table_data_model(cls, table_data_model: TableDataModel) -> DatabaseDataModel:
        os.makedirs(f".db_cache/{table_data_model.id}", exist_ok=True)
        db_path = os.path.join(
            f".db_cache/{table_data_model.id}", os.path.splitext(table_data_model.raw_data_name)[0] + ".db"
        )
        engine = create_engine(f"sqlite:///{db_path}")
        table_data_model.raw_data.to_sql(table_data_model.raw_data_name, engine, if_exists="replace")
        db = SQLDatabase(engine)
        return cls.from_raw_data(raw_data=db, raw_data_name=table_data_model.raw_data_name)

    def insert_table_data_model(self, table_data_model: TableDataModel) -> None:
        engine = self.raw_data.engine
        table_data_model.raw_data.to_sql(table_data_model.raw_data_name, engine)

    def get_llm_side_data(self, serialize_method: str = "database", num_visible_rows: int = 3) -> Any:
        db = self.raw_data
        formatted_db = serialize_db(db, serialize_method, num_visible_rows)
        return formatted_db

    def get_human_side_data(self) -> Any:
        # In the frontend, we show the first few rows of each table
        engine = self.raw_data.engine
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        # Loop through each table name, creating a DataFrame from the first three rows of each table
        df_dict = {}
        for table_name in table_names:
            query = f"SELECT * FROM {table_name} LIMIT 3"
            df = pd.read_sql(query, engine)
            df_dict[table_name] = df
        return df_dict
