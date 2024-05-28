import json

import requests


def call_api(input_json, api_key):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(input_json))

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}


# input_json = {
#     "q": "google inc's stock price",
# }
