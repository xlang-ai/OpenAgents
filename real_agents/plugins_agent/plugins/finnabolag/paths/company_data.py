import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://finna-bolag.fly.dev/get_company_data"
    params = {
        "registration_number": input_json["registration_number"]
    }
    if "is_holding" in input_json:
        params["is_holding"] = input_json["is_holding"]
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
