from typing import List
from flask import jsonify

from backend.app import app

DATA_TOOLS = [
    {
        "type": "language",
        "id": "1cea1f39-fe63-4b08-83d5-fa4c93db0c87",
        "name": "SQLQueryBuilder",
        "name_for_human": "SQL",
        "pretty_name_for_human": "SQL Query Generation",
        "icon": "",
        "description": "Using SQL as the programming language",
    },
    {
        "type": "language",
        "id": "0c135359-af7e-473b-8425-1393d2943b57",
        "name": "PythonCodeBuilder",
        "name_for_human": "Python",
        "pretty_name_for_human": "Python Code Generation",
        "icon": "",
        "description": "Using Python as the programming language",
    },
    {
        "type": "tool",
        "id": "a86aebe1-a780-4038-a333-fb2a9d2d25fc",
        "name": "Echarts",
        "name_for_human": "Echarts",
        "pretty_name_for_human": "Echarts",
        "icon": "",
        "description": "Enhancing the analyzing experience with interactive charts",
    },
    {
        "type": "tool",
        "id": "c7c826ba-5884-4e2b-b27c-fedea30c1749",
        "name": "KaggleDataLoader",
        "name_for_human": "Kaggle Data Search",
        "pretty_name_for_human": "Kaggle Data Search",
        "icon": "",
        "description": "Search & Connect to kaggle datasets",
    },
    {
        "type": "tool",
        "id": "8f8e8dbc-ae5b-4950-9f4f-7f5238978806",
        "name": "DataProfiling",
        "name_for_human": "Data Profiling",
        "pretty_name_for_human": "Data Profiling",
        "icon": "",
        "description": "Intelligent profiling for your data",
    },
]


@app.route("/api/data_tool_list", methods=["POST"])
def get_data_tool_list() -> List[dict]:
    """Gets the data tool list. """
    for i, tool in enumerate(DATA_TOOLS):
        cache_path = f"backend/static/images/{tool['name']}.cache"
        with open(cache_path, 'r') as f:
            image_content = f.read()
            DATA_TOOLS[i]["icon"] = image_content

    return jsonify(DATA_TOOLS)
