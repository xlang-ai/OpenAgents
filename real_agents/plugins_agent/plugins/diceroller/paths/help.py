import requests


def call_api(input_json):
    response = requests.get("https://dmtoolkit.magejosh.repl.co/help")

    if response.status_code == 200:
        return response.text
    else:
        return {"status_code": response.status_code, "text": response.text}
