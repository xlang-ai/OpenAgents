from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> dict:
    url = "https://rising-analogy-387407.uc.r.appspot.com/top_songs"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
