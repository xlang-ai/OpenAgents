from typing import Any

from real_agents.adapters.data_model.base import DataModel


class ImageDataModel(DataModel):
    """A data model for image."""

    simple_filename = ""

    def get_raw_data(self) -> Any:
        return self.raw_data

    def get_llm_side_data(self) -> Any:
        if self.simple_filename == "":
            import os

            self.simple_filename = os.path.basename(self.raw_data_path)
        string = "image: " + self.simple_filename
        return string

    def get_human_side_data(self) -> Any:
        return self.raw_data["base64_string"]
