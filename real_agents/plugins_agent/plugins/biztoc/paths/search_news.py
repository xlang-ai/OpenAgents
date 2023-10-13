"""Search news from Biztoc API."""
from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://ai.biztoc.com/ai/news", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
