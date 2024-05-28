from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post("https://kirill.customgpt.ai/query", json=input_json, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}