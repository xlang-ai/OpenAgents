import requests
from typing import Dict, Any


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://local.goodcall.ai/openapi.yaml")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
