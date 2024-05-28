from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://mtg-rules-chatgpt-plugin.fly.dev/logo.png")

    if response.status_code == 200:
        return response.content
    else:
        return {"status_code": response.status_code, "text": response.text}
