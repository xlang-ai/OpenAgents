import requests


def call_api(input_json, api_key):
    url = "https://alpha-vantage.p.rapidapi.com/query"

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"}

    response = requests.get(url, headers=headers, params=input_json)
    if input_json["datatype"] == "csv":
        return response.text
    elif input_json["datatype"] == "json":
        return response.json()
    else:
        raise Exception("Invalid datatype: " + input_json["datatype"])


# input_json = {"keywords": "microsoft", "function": "SYMBOL_SEARCH", "datatype": "json"}
