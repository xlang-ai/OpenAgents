import requests
from typing import Dict, Any


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.put("https://sentence-beasts.thx.pw/record-match", json=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
