"""Translate a phrase from one language to another."""
from typing import Any, Dict

import requests

url = "https://api.speak.com/v1/public/openai/translate"


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=input_json, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#     "phrase_to_translate": "Hello, how are you?",
#     "learning_language": "Spanish",
#     "native_language": "English",
#     "additional_context": "Casual conversation",
#     "full_query": "How do I say hello, how are you in Spanish?"
# }
