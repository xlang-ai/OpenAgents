from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    asin = input_json.pop("asin")
    response = requests.get(f"https://primeloupe.com/api/v1/get_summary/{asin}", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
