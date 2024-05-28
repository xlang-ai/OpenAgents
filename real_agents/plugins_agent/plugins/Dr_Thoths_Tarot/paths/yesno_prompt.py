import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://dr-thoth-tarot.herokuapp.com/yesno"
    params = {
        "question": input_json.get("question", "")
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
