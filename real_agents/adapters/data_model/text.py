from real_agents.adapters.data_model.base import DataModel


class TextDataModel(DataModel):
    """A data model for text, general purpose."""

    def get_llm_side_data(self, max_chars: int = 5000) -> str:
        assert isinstance(self.raw_data, str)
        return self.raw_data[:max_chars]
