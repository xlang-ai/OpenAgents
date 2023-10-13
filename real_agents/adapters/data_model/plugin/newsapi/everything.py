from copy import deepcopy
from typing import Any, Dict


def convert(_input_json: Dict[str, Any]) -> Dict[str, Any]:
    input_json = deepcopy(_input_json)
    assert isinstance(input_json["out"], list)

    input_json["out"]["articles"] = input_json["out"]["articles"][:5]
    return input_json
