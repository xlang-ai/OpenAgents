import json
from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://qasmshor.onrender.com/BigQubits/qasmshor/queue_in_QASM_generation_task",
                             headers=headers, data=json.dumps(input_json))

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
