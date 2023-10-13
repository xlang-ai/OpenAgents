"""Executor that manage the plugins calling"""
from __future__ import annotations

from typing import Any, Callable, Dict, Union
from pydantic import BaseModel, Extra

from langchain.base_language import BaseLanguageModel

from real_agents.adapters.data_model import SpecModel
from real_agents.plugins_agent import APICallingChain
from real_agents.plugins_agent.plugins.utils import load_plugin_elements_by_name
from real_agents.adapters.data_model.utils import indent_multiline_string


class PluginExecutor(BaseModel):
    """Executor to call plugins that handle the spec showing, endpoint calling and output modeling."""
    name: str
    description: str
    spec_model: SpecModel
    meta_info: Dict[str, Any]
    endpoint2caller: Dict[str, Callable]
    endpoint2output_model: Dict[str, Callable]

    api_key: str = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def full_description(self, add_extra_description_from_plugin=True):
        description = (
            self.description + "\nOpenAPI information:\n" + indent_multiline_string(
                self.spec_model.prepare_spec())
            if add_extra_description_from_plugin
            else self.description
        )
        return description

    @classmethod
    def from_plugin_name(cls, plugin_name: str, ) -> PluginExecutor:
        plugin_info = load_plugin_elements_by_name(plugin_name)

        return cls(
            name=plugin_info["name"],
            description=plugin_info["description"],
            spec_model=plugin_info["spec_model"],
            meta_info=plugin_info["meta_info"],
            endpoint2caller=plugin_info["endpoint2caller"],
            endpoint2output_model=plugin_info["endpoint2output_model"],
        )

    def run(
            self,
            user_intent: str,
            llm: BaseLanguageModel,
    ) -> Union[str, Dict[str, Any]]:
        inputs = {"input_str": user_intent}
        method = APICallingChain.from_llm_and_plugin(
            llm,
            self.meta_info,
            self.spec_model,
            self.endpoint2caller,
            self.endpoint2output_model,
            self.api_key,
        )

        output = method(inputs)
        return output

    def load_personnel_info(self):
        new_endpoint2caller, new_endpoints2output_model = self.spec_model.load_personnel_info(
            api_key=self.api_key)
        self.endpoint2caller = self.endpoint2caller | new_endpoint2caller
        self.endpoint2output_model = self.endpoint2output_model | new_endpoints2output_model
