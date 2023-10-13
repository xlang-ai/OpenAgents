"""Explain the task to the user."""
from typing import Any, Dict

import requests

url = "https://api.speak.com/v1/public/openai/explain-task"


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=input_json, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#         "task_description": "ask for directions,
#         "learning_language": "French",
#         "native_language": "English",
#         "additional_context": "In a city",
#         "full_query": "How do I ask for directions in French?"
#     }
