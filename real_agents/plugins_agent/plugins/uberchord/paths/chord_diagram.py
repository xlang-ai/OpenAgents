import requests
from typing import Dict, Any


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get("https://guitarchords.pluginboost.com/chord-formatted", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
