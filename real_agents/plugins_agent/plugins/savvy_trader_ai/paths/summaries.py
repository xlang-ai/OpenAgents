from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    symbol = input_json.pop("symbol")
    response = requests.get(f"https://api.savvytrader.com/pricing/gpt/assets/{symbol}/summaries", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
