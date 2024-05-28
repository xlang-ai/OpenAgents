from typing import Any, Dict
import requests
import json


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://dr-thoth-tarot.herokuapp.com/occult_card", params=input_json)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {"status_code": response.status_code, "text": response.text}
