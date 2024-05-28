import requests


def call_api(input_json, api_key):
    url = "https://api.polygon.io/v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}"

    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    assert "url_input" in input_json
    url = url.format(**input_json["url_input"])
    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
