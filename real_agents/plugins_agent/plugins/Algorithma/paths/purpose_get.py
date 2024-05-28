from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("http://algorithma.ruvnet.repl.co/purpose")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
