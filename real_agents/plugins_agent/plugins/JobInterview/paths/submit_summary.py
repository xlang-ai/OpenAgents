from typing import Any, Dict

import requests
import json


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://c-interview.copilot.us/api/answers/submit-summary", data=json.dumps(input_json))

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
