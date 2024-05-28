import requests


# Hard for LLm to use, deprecated


def call_api(input_json, api_key):
    input_json["appid"] = api_key
    response = requests.get("https://www.wolframalpha.com/api/v1/query.jsp", params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# query = "What is the population of New York City?"
