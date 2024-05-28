import json
from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    url = "https://paraphraser-best.vercel.app/paraphrase?text=" + input_json["text"]
    response = requests.get(url)
    response_json = json.loads(response.text)

    if response.status_code == 200:
        return response_json
    else:
        return {"status_code": response.status_code, "text": response.text}
