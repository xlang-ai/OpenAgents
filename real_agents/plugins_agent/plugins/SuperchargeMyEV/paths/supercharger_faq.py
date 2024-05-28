from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, any]) -> Dict[str, Any]:
    response = requests.get("https://plugin.charge-my-ev.guide/api/openai/superchargers/frequently-asked-questions")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
