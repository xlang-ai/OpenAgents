from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://chatgpt.boolio.co.kr/api/stock/summary", json=input_json)

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}