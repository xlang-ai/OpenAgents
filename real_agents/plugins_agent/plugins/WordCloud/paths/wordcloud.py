from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        "https://plugin-b0025af30daf4bea989db7074f90b64a-jexkai4vea-uc.a.run.app/wordcloud", json=input_json
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
