from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://spirifyqrcode.azurewebsites.net/api/QRCode/puzzle", json=input_json)
    try:
        return response.json()
    except Exception:
        try:
            return response.text
        except Exception as e:
            return {"status_code": response.status_code, "text": response.text}

