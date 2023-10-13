import json
from copy import deepcopy
from typing import Dict, List

from real_agents.adapters.data_model.base import DataModel


class JsonDataModel(DataModel):
    """A data model for json, general purpose."""

    filter_keys: List[str] = []

    def get_llm_side_data(self, json_format: str = "json") -> str:
        if json_format == "json":
            assert isinstance(self.raw_data, Dict)
            llm_side_data = deepcopy(self.raw_data)
            for key, value in self.raw_data.items():
                if key in self.filter_keys:
                    llm_side_data[key] = "..."
                    continue

                if isinstance(value, DataModel):
                    llm_side_data[key] = value.get_llm_side_data()
                else:
                    llm_side_data[key] = str(value)

            return json.dumps(llm_side_data, indent=4)
        else:
            raise NotImplementedError
