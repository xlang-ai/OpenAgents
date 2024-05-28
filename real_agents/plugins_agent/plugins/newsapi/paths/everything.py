import requests


def call_api(input_json, api_key):
    api_key = api_key
    input_json["apiKey"] = api_key
    response = requests.get("https://newsapi.org/v2/everything/", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}


# input_json = {'q': 'business', 'from': '2023-7-18', 'sortBy': 'relevancy', 'language': 'fr', 'apiKey': 'your-api-key-here', 'page': 1}
