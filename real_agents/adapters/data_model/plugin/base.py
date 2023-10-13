from __future__ import annotations

import json
import os
from typing import Any, Dict

import yaml
from prance import ResolvingParser
from pydantic import BaseModel

# get the absolute path of the current file
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class APIYamlModel(BaseModel):
    info: Dict

    @classmethod
    def from_yaml(cls, yaml_path: str) -> APIYamlModel:
        return cls(info=APIYamlModel.yaml_to_json(yaml_path))

    @classmethod
    def from_json(cls, json_path: str) -> APIYamlModel:
        with open(json_path, "r") as json_file:
            json_data = json.load(json_file)
        return cls(info=json_data)

    def to_yaml(self) -> Dict:
        yaml_data = yaml.safe_dump(self.info, sort_keys=False)
        return yaml_data

    def to_json(self) -> Dict:
        return self.info

    @staticmethod
    def yaml_to_json(yaml_path: str) -> Dict:
        # Open the OpenAPI YAML file
        # Load the YAML contents into a Python dictionary
        # json_data = yaml.safe_load(yaml_file)
        # there are #/xxxx/yyyy reference in openapi.yaml
        parsed = ResolvingParser(yaml_path, backend="openapi-spec-validator", strict=False)
        json_data = json.loads(parsed.json())
        return json_data

    @staticmethod
    def json_to_yaml(json_path: str) -> Any:
        # Open the OpenAPI JSON file
        with open(json_path, "r") as json_file:
            json_data = json.load(json_file)
            yaml_data = yaml.dump(json_data)
            return yaml_data
