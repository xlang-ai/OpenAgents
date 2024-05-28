from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    origin = input_json["origin"]
    destination = input_json["destination"]
    dateStr = input_json["dateStr"]
    response = requests.get(f"https://openai.ferryhopper.com/get-ferries/{origin}/{destination}/{dateStr}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
