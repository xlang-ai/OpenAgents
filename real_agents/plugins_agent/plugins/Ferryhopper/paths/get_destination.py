from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    country = input_json["country"]
    destination = input_json["destination"]
    response = requests.get(f"https://openai.ferryhopper.com/get-destination/{country}/{destination}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
