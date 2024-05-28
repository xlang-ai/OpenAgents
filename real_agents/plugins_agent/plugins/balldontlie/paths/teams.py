import requests


def call_api(input_json):
    response = requests.get("https://balldontlie.io/api/v1/teams", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {"search": "Chicago"}
