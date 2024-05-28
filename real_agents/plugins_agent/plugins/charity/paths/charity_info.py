from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://api.charitysense.com/charity/" + input_json["ein"]
    params = {}
    if "year" in input_json:
        params["year"] = input_json["year"]
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
