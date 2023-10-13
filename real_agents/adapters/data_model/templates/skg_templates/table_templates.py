import subprocess
import sys
from copy import deepcopy
from typing import Any, Dict, Union

import pandas as pd
from sqlalchemy import create_engine
import tiktoken

from real_agents.adapters.schema import SQLDatabase


def convert(
    table_data: Union[pd.DataFrame, Dict[str, Any]], table_name: str = "table", visible_rows_num: int = 3
) -> Dict[str, str]:
    """
    Convert table data to string representations in different formats.

    :param table_data: A dictionary with "cols" (list of strings) and "rows"
                        (list of lists of strings) as keys.
    :param table_name: The name of the table.
    :param visible_rows_num: The number of rows to be displayed in the representation.
    :return: A dictionary with the string table representations in different formats.
    """

    def install_required_packages() -> None:
        packages = ["tabulate", "prettytable"]

        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Call the function to install the required packages
    install_required_packages()
    from prettytable import PrettyTable

    # Handle situation when the table_data is already a dataframe, FIXME: this is a hack
    new_table_data = {}
    if isinstance(table_data, pd.DataFrame):
        new_table_data["cols"] = table_data.columns
        new_table_data["rows"] = table_data.values.tolist()
    table_data = new_table_data

    # Type check for table_data
    if not isinstance(table_data, dict) or "cols" not in table_data or "rows" not in table_data:
        raise TypeError("table_data must be a dictionary with 'cols' and 'rows' as keys.")

    table_data_for_observable = deepcopy(table_data)
    if len(table_data_for_observable["rows"]) > visible_rows_num:
        table_data_for_observable["rows"] = table_data_for_observable["rows"][:visible_rows_num]
        table_data_for_observable["rows"].append(["..."] * len(table_data_for_observable["cols"]))

    # Create dataframe from table_data
    df = pd.DataFrame(table_data_for_observable["rows"], columns=table_data_for_observable["cols"])

    # Generate tables in different formats
    markdown_table = df.to_markdown(index=False)
    html_table = df.to_html(index=False)
    latex_table = df.to_latex(index=False)
    csv_table = df.to_csv(index=False)
    tsv_table = df.to_csv(index=False, sep="\t")
    rest_table = df.to_string(index=False)

    def bbcode_mode_table(data_frame: pd.DataFrame) -> str:
        bbcode_table = "[table]\n"
        for row in data_frame.itertuples(index=False):
            bbcode_table += "[tr]\n"
            for value in row:
                bbcode_table += f"[td]{value}[/td]\n"
            bbcode_table += "[/tr]\n"
        bbcode_table += "[/table]"
        return bbcode_table

    def mediawiki_mode_table(data_frame: pd.DataFrame) -> str:
        mediawiki_table = '{| class="wikitable"\n|-\n'
        for col in data_frame.columns:
            mediawiki_table += f"! {col}\n"
        for row in data_frame.itertuples(index=False):
            mediawiki_table += "|-\n"
            for value in row:
                mediawiki_table += f"| {value}\n"
        mediawiki_table += "|}"
        return mediawiki_table

    def org_mode_table(data_frame: pd.DataFrame) -> str:
        org_table = (
            "| "
            + " | ".join(data_frame.columns)
            + " |\n|-"
            + " | -".join(["-" * len(col) for col in data_frame.columns])
            + " |\n"
        )
        for row in data_frame.itertuples(index=False):
            org_table += "| " + " | ".join([str(value) for value in row]) + " |\n"
        return org_table

    bbcode_table = bbcode_mode_table(df)
    mediawiki_table = mediawiki_mode_table(df)
    org_table = org_mode_table(df)

    pretty_table = PrettyTable()
    pretty_table.field_names = table_data["cols"]
    for row in table_data["rows"]:
        pretty_table.add_row(row)
    pretty_table = str(pretty_table)

    # New function to generate SQL table
    def sql_mode_table(data_frame: pd.DataFrame, _table_name: str) -> str:
        sql_table_str = f"CREATE TABLE {table_name}(\n"

        for col in data_frame.columns:
            sql_table_str += f"{col} text,\n"

        # Remove the last comma and add the primary key constraint
        sql_table_str = sql_table_str[:-2] + f",\nPRIMARY KEY ({data_frame.columns[0]})\n);"

        sql_table_str += "\n/*\n{} example rows:\n".format(len(data_frame))
        for i, _row in data_frame.iterrows():
            _row = "\t".join([str(_cell) for _cell in _row.to_list()])
            sql_table_str += f"{_row}\n"
        sql_table_str += "*/"

        return sql_table_str

    sql_table = sql_mode_table(df, table_name)

    # Return the representation in different formats as a dictionary
    return {
        "Markdown": markdown_table,
        "HTML": html_table,
        "LaTeX": latex_table,
        "CSV": csv_table,
        "TSV": tsv_table,
        "reStructuredText": rest_table,
        "BBCode": bbcode_table,
        "MediaWiki": mediawiki_table,
        "Org mode": org_table,
        "PrettyTable": pretty_table,
        "SQL": sql_table,
    }


def serialize_df(
    table_data: pd.DataFrame,
    table_name: str,
    table_path: str,
    serialize_method: str = "tsv",
    num_visible_rows: int = 3,
    max_tokens: int = 1000,
    data_dir_splitter: str = "backend/data/",
) -> str:
    """Convert dataframe to a string representation."""
    if serialize_method == "tsv":
        # Here it means ignore the "path/to/the/data/<user_id/" part of the path
        pretty_path = "/".join(table_path.split(data_dir_splitter)[-1].strip("/").split("/")[1:])
        string = (
            "Here are table columns and the first {} rows of the table from the path {}"
            '(only a small part of the whole table) called "{}":\n'.format(num_visible_rows, pretty_path, table_name)
        )
        string += table_data.head(num_visible_rows).to_csv(sep="\t", index=False)
        # Truncate the string if it is too long
        enc = tiktoken.get_encoding("cl100k_base")
        enc_tokens = enc.encode(string)
        if len(enc_tokens) > max_tokens:
            string = enc.decode(enc_tokens[:max_tokens])
    elif serialize_method == "database":
        engine = create_engine("sqlite:///:memory:")
        table_data.to_sql(table_name, engine)
        db = SQLDatabase(engine)
        # TODO: Now access the internal variable
        setattr(db, "_sample_rows_in_table_info", num_visible_rows)
        string = db.get_table_info()
    else:
        raise ValueError("Unknown serialization method.")
    return string
