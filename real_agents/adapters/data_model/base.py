from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel


class DataModel(BaseModel):
    """Base class for data models."""

    id: str
    raw_data: Any
    raw_data_name: str
    raw_data_path: str
    llm_side_data: Any  # could be string or potentially images for future needs
    human_side_data: Any

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_raw_data(
        cls, raw_data: Any, raw_data_name: str = "<default_name>", raw_data_path: str = "<default_path>", **kwargs: Any
    ) -> DataModel:
        uid = str(uuid.uuid4())
        return cls(id=uid, raw_data=raw_data, raw_data_name=raw_data_name, raw_data_path=raw_data_path, **kwargs)

    def get_id(self) -> str:
        return self.id

    def get_raw_data(self) -> Any:
        return self.raw_data

    def get_llm_side_data(self) -> Any:
        return self.raw_data

    def get_human_side_data(self) -> Any:
        return self.raw_data

    def __str__(self) -> str:
        return self.get_llm_side_data()
