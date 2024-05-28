import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://www.appypie.com/v1", params=input_json)

    if response.status_code == 200:
        return response.json()
