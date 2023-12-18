from typing import Any, List

from real_agents.adapters.data_model.base import DataModel


class DocumentDataModel(DataModel):
    """A data model for a document (can contain text, images, tables, other data)."""

    def get_raw_data(self) -> Any:
        return self.raw_data

    def get_llm_side_data(self, 
                          max_tokens: int = 2000,
                          chunk_size: int = 1000, 
                          chunk_overlap: int = 200
                          ) -> Any:
        return self.raw_data['plain_text'][:max_tokens]
