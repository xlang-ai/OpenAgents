import requests


def call_api(input_json):
    response = requests.get("https://local.goodcall.ai/logo.png")

    if response.status_code == 200:
        return response.content
    else:
        return {"status_code": response.status_code, "text": response.text}
