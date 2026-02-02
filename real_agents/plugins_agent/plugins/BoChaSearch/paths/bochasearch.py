import json
import requests

def call_api(input_json, api_key):
    """
    Perform a web search using the Bocha Web Search API.

    Parameters:
    - input_json (dict): Dictionary containing search parameters. Expected keys:
        * query (str): Search query keywords
        * freshness (str): Time range filter for results (e.g., "noLimit")
        * summary (bool): Whether to include text summaries
        * count (int): Number of search results to return
    - api_key (str): API key for authentication

    Returns:
    - dict: Search results containing detailed information such as webpage title, URL, snippet,
            site name, site icon, publication time, etc. On failure, returns a dictionary with
            'status_code' and 'text' fields.
    """

    url = 'https://api.bochaai.com/v1/web-search'  # Fixed trailing whitespace
    headers = {
        'Authorization': f'Bearer {api_key}',  # Replace with your API key
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=input_json)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}