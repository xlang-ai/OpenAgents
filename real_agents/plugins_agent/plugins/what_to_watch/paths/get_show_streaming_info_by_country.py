import requests
from typing import Any, Dict


def call_api(country: str, show_name: str) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    url = f"https://gpt-show-search.fly.dev/streaming/{country}/{show_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
