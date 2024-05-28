from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    owner = input_json["owner"]
    repo = input_json["repo"]
    response = requests.get(f"https://chat-gpt-github-stat-plugin.vercel.app/api/github/{owner}/{repo}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
