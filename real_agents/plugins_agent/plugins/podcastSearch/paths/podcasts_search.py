import requests
from typing import Dict, Any


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://esne.ai/podcasts/" + input_json["podcasttitle"]
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
