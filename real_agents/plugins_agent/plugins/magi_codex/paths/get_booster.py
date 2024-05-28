from typing import Any, Dict

import requests


def call_api(input_json: str) -> Dict[str, Any]:
    set_code = input_json["set_code"]
    response = requests.get(f"https://mtg-rules-chatgpt-plugin.fly.dev/booster/{set_code}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}