"""LLM API for Wolfram Alpha"""
import requests


def call_api(input_json, api_key):
    input_json["appid"] = api_key
    response = requests.get("https://www.wolframalpha.com/api/v1/llm-api", params=input_json)

    if response.status_code == 200:
        return response.content.decode("utf-8")
    else:
        return {"status_code": response.status_code, "text": response.text}
