import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.earth-plugin.com/map-from-coordinates", headers=headers, json=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}