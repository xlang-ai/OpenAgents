from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    owner = input_json.get("owner", "")
    repo = input_json.get("repo", "")
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
