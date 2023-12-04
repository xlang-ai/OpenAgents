from typing import Any, List

from real_agents.adapters.data_model.base import DataModel
from real_agents.data_agent.executors.data_summary_executor import DocumentSummaryExecutor
from langchain.base_language import BaseLanguageModel
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain.chains import ReduceDocumentsChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter



class DocumentDataModel(DataModel):
    """A data model for a document (can contain text, images, tables, other data)."""

    def get_raw_data(self) -> Any:
        return self.raw_data

    def get_llm_side_data(self, 
                          max_tokens: int = 5000, 
                          chunk_size: int = 1000, 
                          chunk_overlap: int = 200
                          ) -> Any:
        return self.raw_data['plain_text'][:max_tokens]
