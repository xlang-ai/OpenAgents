import requests
from typing import Any, Dict, List
from datetime import datetime


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    ticker = input_json.pop('ticker')
    url = f"https://statisfinapp.herokuapp.com/price_change/{ticker}"
    response = requests.get(url, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
