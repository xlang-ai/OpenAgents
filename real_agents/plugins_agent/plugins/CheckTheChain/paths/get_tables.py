from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    dataset_id = input_json["datasetId"]
    response = requests.get(f"https://nani.ooo/api/datasets/{dataset_id}/tables")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
