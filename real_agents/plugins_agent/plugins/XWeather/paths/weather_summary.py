"""Weather summary path for XWeather plugin."""
from typing import Any, Dict
import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://openai-plugin.xweather.com/weather/summary/{}".format(input_json['location'])
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
