"""Utils for plugins (loading and more to add)"""
import importlib
import json
import os
import sys
from collections import defaultdict
from typing import Any
import yaml
from tqdm import tqdm

from real_agents.adapters.data_model import APIYamlModel, SpecModel
from real_agents.plugins_agent.plugins.plugin_names import PluginName

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

AI_PLUGIN_FILE = "ai-plugin.json"
PLUGIN_SPEC_FILE = "openapi.yaml"
PATH_FOLDER = "paths"


def _load_module(name: str, file_path: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, file_path)
    ret = importlib.util.module_from_spec(spec)
    sys.modules[name] = ret
    spec.loader.exec_module(ret)
    return ret


def load_plugin_elements_by_name(plugin_name: str):
    # Check if the plugin name is valid
    assert plugin_name in PluginName.__members__, "Unknown plugin name {}.".format(plugin_name)
    plugin_dir_name = PluginName[plugin_name].value

    # Load in the plugin meta info
    plugin_file_path = os.path.join(CURRENT_PATH, plugin_dir_name)
    data_model_file_path = os.path.join(CURRENT_PATH, "..", "data_model", "plugin", plugin_dir_name)

    meta_info_path = os.path.join(plugin_file_path, AI_PLUGIN_FILE)
    assert os.path.exists(meta_info_path), f"Missing file {meta_info_path} that contains meta info for {plugin_name}"
    with open(meta_info_path, "r") as f:
        meta_info = json.load(f)

        # Load all supported endpoints
    tmp = _load_module(plugin_dir_name, os.path.join(plugin_file_path, "paths", "__init__.py"))
    assert hasattr(tmp, "path_dict"), f"Missing variable path_dict in __init__.py"

    # Load in the plugin spec
    yaml_path = os.path.join(plugin_file_path, PLUGIN_SPEC_FILE)
    assert os.path.exists(yaml_path), f"Missing file: {yaml_path}"

    # fixme: Ugly here, change the whole logic of SpecModel and APIYamlModel to refactor this
    # Load yaml from yaml_path
    openapi_yaml_json = APIYamlModel.from_yaml(yaml_path).to_json()
    if sorted(list(openapi_yaml_json["paths"].keys())) != sorted(list(tmp.path_dict.values())):
        print(f"{yaml_path} and {plugin_dir_name}/paths/__init__.py do not match. Load the later.")
        # Create a new yaml file with only the endpoints in path_dict
        openapi_yaml_json["paths"] = {
            path: openapi_yaml_json["paths"][path] for path in tmp.path_dict.values()
        }
        new_yaml_file_path = os.path.join(plugin_file_path, "tmp", "openapi.yaml")
        os.makedirs(os.path.dirname(new_yaml_file_path), exist_ok=True)
        with open(new_yaml_file_path, "w") as f:
            # Save in the new yaml file, in yaml format
            yaml.safe_dump(openapi_yaml_json, f, sort_keys=False)
        yaml_path = new_yaml_file_path

    spec_model = SpecModel(yaml_path)
    description = spec_model.full_spec["info"]["description"] if "description" in spec_model.full_spec[
        "info"] else "No description."

    filename2endpoint = tmp.path_dict
    endpoint2caller = {}
    endpoint2output_model = defaultdict(lambda x: x)
    for fn, ep in filename2endpoint.items():
        # load api callers for different endpoints
        tmp = _load_module(f"{plugin_dir_name}:{fn}:caller", os.path.join(plugin_file_path, "paths", fn + ".py"))
        assert hasattr(tmp, "call_api"), f"Missing function call_api in {fn}.py"
        endpoint2caller[ep] = tmp.call_api

        # load output data model for different endpoints
        data_model_path = os.path.join(data_model_file_path, fn + ".py")
        if not os.path.exists(data_model_path):
            output_model = lambda x: x
        else:
            tmp = _load_module(f"{plugin_dir_name}:{fn}:output_model", data_model_path)
            assert hasattr(tmp, "convert"), f"Missing function convert in {fn}.py"
            output_model = tmp.convert
        endpoint2output_model[ep] = output_model

    need_auth = meta_info["manifest"]["auth"]["type"] not in [None, "None", "none", "Null", "null"]

    return {
        "name": plugin_name,
        "description": description,
        "meta_info": meta_info,
        "spec_model": spec_model,
        "endpoint2caller": endpoint2caller,
        "endpoint2output_model": endpoint2output_model,
        "need_auth": need_auth,
    }


def load_all_plugins_elements():
    all_plugins_elements = {}

    for plugin_name in tqdm(PluginName.__members__):
        try:
            all_plugins_elements[plugin_name] = load_plugin_elements_by_name(plugin_name)
        except Exception as e:
            print(f"Error when loading plugin {plugin_name}: {e}")

    return all_plugins_elements
