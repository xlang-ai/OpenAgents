"""Explains a foreign phrase in the context of a full query."""
from typing import Any, Dict

import requests

url = "https://api.speak.com/v1/public/openai/explain-phrase"


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=input_json, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#         "foreign_phrase": "no mames",
#         "learning_language": "Spanish",
#         "native_language": "English",
#         "additional_context": "Informal conversation",
#         "full_query": "What does no mames mean in English?"
#     }
