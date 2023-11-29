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
        formatted_doc = construct_doc(self.raw_data, max_tokens, chunk_size, chunk_overlap)
        return formatted_doc


def construct_doc(data: str, llm: BaseLanguageModel, chunk_size: int, chunk_overlap: int):
    reduce_template = """The following is set of summaries:
        {doc_summaries}
        Provide a succinct summary of the provided text with less than 100 words. Please ensure your summary is a complete sentence and include it within <summary></summary> tags."
            
        Begin.
        """
    reduce_chain, map_chain = DocumentSummaryExecutor().text_summary(llm, reduce_template)
    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries"
    )

    # # Combines and iteravely reduces the mapped documents
    # reduce_documents_chain = ReduceDocumentsChain(
    #     # This is final chain that is called.
    #     combine_documents_chain=combine_documents_chain,
    #     # If documents exceed context for `StuffDocumentsChain`
    #     collapse_documents_chain=combine_documents_chain,
    #     # The maximum number of tokens to group documents into.
    #     token_max=max_tokens,
    # )
    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=combine_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="doc_summaries",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    split_docs = text_splitter.split_documents(data['plain_text'])
    map_reduce_chain.run(split_docs) 
