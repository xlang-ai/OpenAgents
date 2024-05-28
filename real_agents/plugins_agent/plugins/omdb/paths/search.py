import requests


def call_api(input_json, api_key):
    input_json["apikey"] = api_key

    response = requests.get("http://www.omdbapi.com/", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {'t': 'The Godfather', 'apiKey': 'key here'}
