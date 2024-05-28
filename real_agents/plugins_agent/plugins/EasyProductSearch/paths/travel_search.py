from typing import Any, Dict
import requests


def call_api(input_json: Dict) -> Dict[str, Any]:
    username = input_json["username"]
    url = f"https://easy-search.techno-gauss.com/api/travel-search/{username}"
    response = requests.get(url, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
