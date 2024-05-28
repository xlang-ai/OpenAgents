from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    address = input_json["address"]
    response = requests.get(f"https://chat.cryptomation.com/api/balance/{address}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
