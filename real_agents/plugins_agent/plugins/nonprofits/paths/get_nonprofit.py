from typing import Any, Dict
import requests


def call_api(nonprofit_id: str) -> Dict[str, Any]:
    response = requests.get(f"https://api.getchange.io/api/v1/openai/nonprofits/{nonprofit_id}")

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
