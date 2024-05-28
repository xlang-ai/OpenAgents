from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    message_id = input_json["message_id"]
    response = requests.delete(f"https://messagesinbottles.space/keep_message/{message_id}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
