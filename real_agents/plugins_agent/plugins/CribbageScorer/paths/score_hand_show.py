import json
from typing import Any, Dict, List
import requests

def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    hand = input_json["hand"]
    isCrib = input_json["isCrib"]
    starter = input_json["starter"]
    # Transform input into required format
    query_params = {"hand": ",".join(hand), "isCrib": str(isCrib), "starter": starter}
    # Make request
    response = requests.post("https://cribbage.azurewebsites.net/score_hand_show", json=query_params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}