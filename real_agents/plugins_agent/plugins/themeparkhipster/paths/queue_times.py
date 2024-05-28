from typing import Any, Dict
import requests


def call_api(input_json: Dict) -> Dict[str, Any]:
    park_id = input_json["park_id"]
    response = requests.get(f"https://plugin.themeparkhipster.com/parks/{park_id}/queue_times")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
