"""Search Coursera API for courses matching a query."""
from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://www.coursera.org/api/rest/v1/search", json=input_json)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
