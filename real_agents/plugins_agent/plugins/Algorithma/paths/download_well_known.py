from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    file_name = input_json["file_name"]
    url = "https://algorithma.ruvnet.repl.co/.well-known/" + file_name
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}