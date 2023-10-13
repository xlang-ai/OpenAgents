"""Search Actions"""
from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any], api_key) -> Dict[str, Any]:
    headers = {
        "X-API-Key": api_key,
    }
    url = "https://nla.zapier.com/api/v1/search/actions/"
    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
