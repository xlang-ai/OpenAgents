from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://chat.jopilot.net/api/chat/search", json=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#     "jobTitlesPositive": ["software engineer", "software developer"],
#     "jobTitlesNegative": ["sales", "marketing"],
#     "locationsPositive": [{"country": "United States", "state": "California", "city": "San Francisco"}]
# }
