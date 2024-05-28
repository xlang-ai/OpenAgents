import requests
from typing import Any, Dict
import json


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    ticker = input_json['ticker']
    url = f"https://statisfinapp.herokuapp.com/volatility/{ticker}"
    response = requests.get(url, params=input_json)
    response_dict = json.loads(response.text)

    if response.status_code == 200:
        return response_dict
    else:
        return {"status_code": response.status_code, "text": response.text}
