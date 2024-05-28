from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = f"https://rising-analogy-387407.uc.r.appspot.com/top_songs/{input_json['country']}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
