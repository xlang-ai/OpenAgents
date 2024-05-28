import requests
from typing import Any, Dict


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    track_id = input_json["track_id"]
    response = requests.get("https://rising-analogy-387407.uc.r.appspot.com/similar_songs/" + str(track_id))

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
