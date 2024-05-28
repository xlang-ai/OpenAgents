from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get(f"https://artcollection--chao-gu-ge-lei.repl.co/{input_json['query']}")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
