import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    city = input_json["city"]
    state = input_json.get("state", "")
    country = input_json["country"]
    url = "https://weather--vicentescode.repl.co/weathernow?city={}&state={}&country={}".format(city, state, country)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
