"""Search for products by keyword, price range, and size."""
from typing import Any, Dict

import requests

url = "https://www.klarna.com/us/shopping/public/openai/v0/products"


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=input_json)

    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}

# input_json = {
#     "q": "nike shoes",
#     "size": 10,
#     "min_price": 50,
#     "max_price": 100
# }
