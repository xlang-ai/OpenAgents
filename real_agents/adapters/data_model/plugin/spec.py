import os
from typing import Any, Dict
import importlib.util
import tiktoken

from real_agents.adapters.data_model.plugin.base import APIYamlModel
from real_agents.adapters.data_model.utils import indent_multiline_string


def import_function_from_file(filepath, function_name):
    spec = importlib.util.spec_from_file_location("module.name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function = getattr(module, function_name)

    return function


def process_one_param(param_dict: Dict[str, Any]) -> str:
    name = param_dict.get("name", None)
    description = param_dict.get("description", None)
    required = param_dict.get("required", None)

    schema = param_dict.get("schema", {})
    type = schema.get("type", "UnknownType")
    value_choices = schema.get("enum", [])

    ret = (
        f"`{name}` ({type}, {'required' if required else 'optional'}): {description}."
        f"{'Examples:' + ','.join([str(_) for _ in value_choices]) if len(value_choices) > 0 else ''}"
    )
    return ret


def process_one_property(name: str, value_dict: Dict[str, Any]) -> str:
    description = value_dict.get("description", None)
    required = value_dict.get("required", None)

    type = value_dict.get("type", "UnknownType")
    value_choices = value_dict.get("enum", [])

    ret = (
        f"`{name}` ({type}, {'required' if required else 'optional'}): {description}."
        f"{'Examples:' + ','.join(value_choices) if len(value_choices) > 0 else ''}"
    )
    return ret


class SpecModel:
    def __init__(self, yaml_path: str, model_name: str = "gpt-4") -> None:
        # fixme: Must move out the logic of yaml path
        self.yaml_path = yaml_path
        self.full_spec = APIYamlModel.from_yaml(yaml_path).to_json()
        self.paths = self.full_spec["paths"]

        # Process the description
        enc = tiktoken.encoding_for_model(model_name)
        if "description" in self.full_spec["info"]:
            if len(self.full_spec["info"]["description"]) > 200:
                self.full_spec["info"]["description"] = enc.decode(
                    enc.encode(self.full_spec["info"]["description"])[:200]
                )

    def load_personnel_info(self, api_key: str):
        # Get the dir of the yaml file
        yaml_dir = os.path.dirname(self.yaml_path)
        personnel_load_dir = os.path.join(yaml_dir, "personnel.py")

        if not os.path.exists(personnel_load_dir):
            return {}, {}

        # Reload openapi.yaml
        reload_openapi = import_function_from_file(personnel_load_dir, "reload_openapi")
        resolved_json, new_paths_json = reload_openapi(api_key, self.full_spec)
        self.full_spec = resolved_json
        self.full_spec["info"] = resolved_json["info"]
        self.paths = resolved_json["paths"]

        # Reload the endpoints functions
        reload_endpoints = import_function_from_file(personnel_load_dir, "reload_endpoints")
        new_endpoint2caller = reload_endpoints(new_paths_json)

        # Reload the endpoints datamodels
        # todo: Add reload datamodels function
        new_endpoints2output_model = {k: lambda x: x for k in new_paths_json}

        return new_endpoint2caller, new_endpoints2output_model

    def prepare_spec(self, include_params: bool = True) -> str:
        path_names = list(self.paths.keys())
        ret = self.prepare_spec_for_one_path(path_names[0], include_params=include_params)

        if len(path_names) > 1:
            ret += "\n"

        for path_name in path_names[1:]:
            ret += (
                self.prepare_spec_for_one_path(path_name, include_api_info=False, include_params=include_params) + "\n"
            )

        return ret

    def list_endpoints(self) -> str:
        ret = ""
        for ep, ep_spec in self.paths.items():
            assert len(ep_spec) == 1, "Support two request methods!"
            request_method = list(ep_spec.keys())[0]
            func_spec = ep_spec[request_method]
            desc = func_spec.get("summary", None)
            ret += f"`{ep}`: {desc}\n"
        return ret.strip()

    def prepare_spec_for_one_path(
        self,
        path_name: str,
        include_api_info: bool = True,
        include_params: bool = True,
    ) -> str:
        func_dict = self.paths[path_name]
        if "servers" in func_dict:
            del func_dict["servers"]

        rets = []
        for request_method in list(func_dict.keys()):
            candidate_inputs_str = ""
            func_spec = func_dict[request_method]

            # Only GET and DELETE are processed, others are not properly processed
            if request_method.lower() not in ["get", "post", "put", "patch", "delete"]:
                raise ValueError("Unknown request method")

            # TODO: not sure how to arrange input when post method has "parameters"
            func_summary = func_spec.get("summary", None)
            func_description = func_spec.get("description", None)
            candidate_inputs = func_spec.get("parameters", [])
            candidate_inputs_str += "\n".join(process_one_param(p) for p in candidate_inputs)

            if request_method.lower() == "post" and "requestBody" in func_spec:
                request_body = func_spec["requestBody"]
                assert "content" in request_body, "Must have content in requestBody"
                content_dict = request_body["content"]
                assert len(content_dict) == 1, "Support one content type"
                content_type = list(content_dict.keys())[0]
                content = content_dict[content_type]
                assert "schema" in content, "Must have schema in requestBody"
                if "properties" in content["schema"]:
                    properties = content["schema"]["properties"]
                    candidate_inputs_str += "\n".join(process_one_property(n, vd) for n, vd in properties.items())

            ret = ""
            if include_api_info:
                ret += f"""Name: {self.full_spec["info"]["title"]}\n{'Description: ' + self.full_spec["info"]['description'] if
                "description" in self.full_spec["info"] else ""}\n"""

            ret += f"""\tSummary: {func_summary}\n"""
            ret += f"""\tDescription: {func_description}\n"""
            candidate_inputs_str = "None" if len(candidate_inputs_str) == 0 else candidate_inputs_str
            ret += (
                f"""\tInput: \n{indent_multiline_string(candidate_inputs_str, indent=2)}\n""" if include_params else ""
            )
            rets.append(ret)

        return f"""Endpoint: {path_name}\n""" + "\n".join(rets)
