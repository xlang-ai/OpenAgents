import requests


def call_api(input_json, api_key):
    url = "https://twelve-data1.p.rapidapi.com/exchanges"

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"}

    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        if "format" in input_json:
            if input_json["format"]:
                if input_json["format"].lower() == "json":
                    return response.json()
                else:
                    return response.text
            else:
                return response.json()
        else:
            return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
