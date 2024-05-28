from typing import Any, Dict, List
import requests


def call_api(used_words: List[str]) -> Dict[str, Any]:
    url = "https://crafty-clues.jeevnayak.repl.co/new_word"
    params = {"used_words": used_words}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}
