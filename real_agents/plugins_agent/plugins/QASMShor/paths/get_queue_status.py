from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    queue_id = input_json.pop("queueID")
    response = requests.get(f"https://qasmshor.onrender.com/BigQubits/qasmshor/get_queue_status/{queue_id}",
                            params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
