from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        "https://plugin-3c56b9d4c8a6465998395f28b6a445b2-jexkai4vea-uc.a.run.app/upload_and_search_pdf",
        json=input_json,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
