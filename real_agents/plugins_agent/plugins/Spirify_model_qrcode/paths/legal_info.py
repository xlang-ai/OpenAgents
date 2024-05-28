import requests


def call_api(input_json=None):
    response = requests.get("https://spirifyqrcode.azurewebsites.net/LegalInfo")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
