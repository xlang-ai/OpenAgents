from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    params = {}
    if "trends" in input_json:
        params["trends"] = input_json["trends"]
    response = requests.get("https://traders-insight.vercel.app/stocks", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
