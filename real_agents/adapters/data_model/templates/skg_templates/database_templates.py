import sqlite3
from typing import Dict, Union

import pandas as pd
import tiktoken


from real_agents.adapters.data_model.templates.skg_templates.table_templates import (
    convert as convert_table,
)
from real_agents.adapters.schema import SQLDatabase


def convert(db_input: Union[str, Dict[str, pd.DataFrame]], visible_rows_num: int = 3) -> Dict[str, str]:
    """
    Convert database data to string representations in different formats.

    :param db_input: the path to the sqlite database file, or a pd.DataFrame.
    :param visible_rows_num: the number of rows to be displayed in each table.
    :return: A dictionary with the string database representations in different formats.
    """
    if isinstance(db_input, str):
        conn = sqlite3.connect(db_input)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = [name[0] for name in cursor.fetchall()]
        dfs = {table_name: pd.read_sql_query(f"SELECT * FROM {table_name}", conn) for table_name in table_names}
    elif isinstance(db_input, dict) and all(isinstance(df, pd.DataFrame) for df in db_input.values()):
        dfs = db_input
    else:
        raise ValueError("db_input should be either a SQLite database file path or a dictionary of pandas DataFrames")

    representations = {
        "Markdown": "",
        "HTML": "",
        "LaTeX": "",
        "CSV": "",
        "TSV": "",
        "reStructuredText": "",
        "BBCode": "",
        "MediaWiki": "",
        "Org mode": "",
        "PrettyTable": "",
        "SQL": "",
    }

    for table_name, df in dfs.items():
        table_data = {"cols": df.columns.tolist(), "rows": df.values.tolist()}
        table_representations = convert_table(table_data, table_name, visible_rows_num)
        for _format, table_representation in table_representations.items():
            representations[_format] += table_representation + "\n\n"

    return representations


def serialize_db(
    db: SQLDatabase,
    serialize_method: str = "database",
    num_visible_rows: int = 3,
    max_tokens: int = 1000,
) -> str:
    """Convert database engine to a string representation."""
    if serialize_method == "database":
        # TODO: Now access the internal variable
        setattr(db, "_sample_rows_in_table_info", num_visible_rows)
        string = db.get_table_info()
        # Truncate the string if it is too long
        enc = tiktoken.get_encoding("cl100k_base")
        enc_tokens = enc.encode(string)
        if len(enc_tokens) > max_tokens:
            string = enc.decode(enc_tokens[:max_tokens])
    else:
        raise ValueError("Unknown serialization method.")
    return string
