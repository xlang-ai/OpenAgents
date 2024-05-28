import requests


def call_api(input_json, api_key):
    url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "youtube-search-results.p.rapidapi.com"}

    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {"q": "Andrew Ng & OpenAI: prompt engineering"}
