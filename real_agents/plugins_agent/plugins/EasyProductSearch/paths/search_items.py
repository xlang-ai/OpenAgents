import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    username = input_json["username"]
    url = "https://easy-search.techno-gauss.com/api/search/{}".format(username)
    headers = {
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}