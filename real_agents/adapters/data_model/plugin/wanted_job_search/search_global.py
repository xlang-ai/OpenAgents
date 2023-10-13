from copy import deepcopy
from typing import Any, Dict


def convert(_input_json: Dict[str, Any]) -> Dict[str, Any]:
    input_json = deepcopy(_input_json)
    assert isinstance(input_json["out"], list)

    input_json["out"] = input_json["out"][:5]

    for i, job in enumerate(input_json["out"]):
        cleaned_job_item = input_json["out"][i]
        del cleaned_job_item["id"]
        del cleaned_job_item["created"]
        input_json["out"][i] = cleaned_job_item

    return input_json
