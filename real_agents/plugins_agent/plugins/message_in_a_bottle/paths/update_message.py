from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    message_id = input_json.pop("message_id")
    response = requests.put(f"https://messagesinbottles.space/update_message/{message_id}", json=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
