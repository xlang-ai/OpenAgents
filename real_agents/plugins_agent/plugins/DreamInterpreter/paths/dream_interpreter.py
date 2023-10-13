"""Dream Interpreter plugin."""
from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    dream_text = input_json["DreamText"]
    response = requests.get(f"https://dreamplugin.bgnetmobile.com/getDream/{dream_text}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
