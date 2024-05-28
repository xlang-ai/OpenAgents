from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    api_url = "https://companieshouse.tradexy.repl.co/search"

    headers = {"Accept": "application/json"}

    params = {
        "q": input_json["q"],
        "items_per_page": input_json.get("items_per_page", 10),
        "start_index": input_json.get("start_index", 0),
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
