from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    datasetId = input_json["datasetId"]
    tableId = input_json["tableId"]
    response = requests.get(f"https://nani.ooo/api/datasets/{datasetId}/tables/{tableId}/schema")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
