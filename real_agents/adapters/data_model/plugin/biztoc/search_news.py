from copy import deepcopy
from typing import Any, Dict


def convert(_input_json: Dict[str, Any]) -> Dict[str, Any]:
    input_json = deepcopy(_input_json)
    assert isinstance(input_json["out"], list)

    input_json["out"] = input_json["out"][:5]
    extracted_keys = [
        "body",
        "title",
        "created",
        "url",
        "tags",
    ]
    input_json["out"] = [{k: r[k] for k in extracted_keys if k in r} for r in input_json["out"]]
    return input_json
