import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://openai.jettel.de/youtube/getVideoSummary"
    response = requests.get(url, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
