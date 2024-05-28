import requests


def call_api(input_json, api_key):
    url = "https://skyscanner-api.p.rapidapi.com/v3/flights/live/search/create"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com",
    }
    input_json = {"query": input_json}

    response = requests.post(url, json=input_json, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
# 		"market": "UK",
# 		"locale": "en-GB",
# 		"currency": "EUR",
# 		"queryLegs": [
# 			{
# 				"originPlaceId": { "iata": "LON" },
# 				"destinationPlaceId": { "iata": "DXB" },
# 				"date": {
# 					"year": 2023,
# 					"month": 9,
# 					"day": 20
# 				}
# 			}
# 		],
# 		"cabinClass": "CABIN_CLASS_ECONOMY",
# 		"adults": 2,
# 		"childrenAges": [3, 9]
# 	}
