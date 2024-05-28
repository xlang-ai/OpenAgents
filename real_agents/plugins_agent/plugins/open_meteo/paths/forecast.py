import requests


def call_api(input_json):
    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#         "latitude": 52.5200,
#         "longitude": 13.4050,
#         "hourly": ["temperature_2m", "windspeed_10m", "precipitation"],
#         "daily": ["temperature_2m_min", "temperature_2m_max", "precipitation_sum"],
#         "current_weather": "true",
#         "timezone": "Europe/Berlin"
#     }
