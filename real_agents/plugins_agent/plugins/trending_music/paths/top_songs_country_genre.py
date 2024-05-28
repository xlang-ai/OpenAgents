import requests
from typing import Dict, Any


def call_api(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://rising-analogy-387407.uc.r.appspot.com/top_songs/" + input_dict["country"] + "/" + input_dict[
        "genre"]
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
