import requests


def call_api(input_json, api_key):
    url = "https://api-nba-v1.p.rapidapi.com/leagues"

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {}
