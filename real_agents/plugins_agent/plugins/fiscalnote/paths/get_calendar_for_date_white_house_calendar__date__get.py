from typing import Any, Dict
import requests


def call_api(date: str) -> Dict[str, Any]:
    response = requests.get(f"https://api.factba.se/white-house/calendar/{date}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
