from typing import Any, Dict, Tuple, Union
from abc import ABC

from langchain.base_language import BaseLanguageModel
from langchain import PromptTemplate

from real_agents.adapters.callbacks.executor_streaming import ExecutorStreamingChainHandler
from real_agents.adapters.data_model import DatabaseDataModel, TableDataModel, ImageDataModel
from real_agents.adapters.llm import LLMChain


class DataSummaryExecutor(ABC):
    tool_name = "DataProfiling"

    def _intelligent_summary(self, grounding_source: ImageDataModel, num_insights: int, llm: BaseLanguageModel) -> str:
        """Use LLM to generate data summary."""
        pass


class TableSummaryExecutor(DataSummaryExecutor):
    SUMMARY_PROMPT_TEMPLATE = """
{table_info}

Provide a succinct yet meaningful summary of the table with less than 20 words, encapsulating its essence beyond just enumerating the columns. Please ensure your summary is a complete sentence and include it within <summary></summary> tags."
Note the table actually far more rows than shown above, so you MUST NOT make any rash conclusions based on the shown table rows or cells."
Then provide {num_insights} insightful and interesting suggestions in natural language that users can directly say to analyze the table. The suggestions should be able to be solved by python/sql."
The final results should be markdown '+' bullet point list, e.g., + The first suggestion.

Begin."
"""
    stream_handler = ExecutorStreamingChainHandler()

    def run(
        self,
        grounding_source: Union[TableDataModel, DatabaseDataModel],
        llm: BaseLanguageModel,
        use_intelligent_summary: bool = True,
        num_insights: int = 3,
    ) -> Dict[str, Any]:
        summary = ""
        if isinstance(grounding_source, TableDataModel):
            df = grounding_source.raw_data
            df_name = grounding_source.raw_data_name
            # Basic summary
            summary += f"Your table {df_name} contains {df.shape[0]} rows and {df.shape[1]} columns. "

            null_count = df.isnull().sum().sum()  # Get total number of null values
            unique_values_avg = df.nunique().mean()  # Get average number of unique values

            summary += f"On average, each column has about {unique_values_avg:.0f} unique values. "
            if null_count > 0:
                summary += f"Watch out, there are {null_count} missing values in your data. "
            else:
                summary += "Good news, no missing values in your data. "

            # Intelligent summary
            if use_intelligent_summary:
                intelligent_summary = self._intelligent_summary(
                    grounding_source,
                    num_insights=num_insights,
                    llm=llm,
                )
                table_summary, suggestions = self._parse_output(intelligent_summary)
                summary += table_summary
                summary += "\n" + "Here are some additional insights to enhance your understanding of the table."
                summary += "\n" + suggestions

            for stream_token in summary.split(" "):
                self.stream_handler.on_llm_new_token(stream_token)

        elif isinstance(grounding_source, DatabaseDataModel):
            # TODO: Convert to df or use SQL query for basic summary
            raise NotImplementedError("DatabaseDataModel is not supported yet.")
        else:
            raise ValueError(f"Unsupported grounding source type: {type(grounding_source)}")
        return summary

    def _intelligent_summary(
        self, grounding_source: Union[TableDataModel, DatabaseDataModel], num_insights: int, llm: BaseLanguageModel
    ) -> str:
        """Use LLM to generate data summary."""
        summary_prompt_template = PromptTemplate(
            input_variables=["table_info", "num_insights"],
            template=self.SUMMARY_PROMPT_TEMPLATE,
        )
        method = LLMChain(llm=llm, prompt=summary_prompt_template)
        result = method.run({"table_info": grounding_source.get_llm_side_data(), "num_insights": num_insights})
        return result

    def _parse_output(self, content: str) -> Tuple[str, str]:
        """Parse the output of the LLM to get the data summary."""
        from bs4 import BeautifulSoup

        # Using 'html.parser' to parse the content
        soup = BeautifulSoup(content, "html.parser")
        # Parsing the tag and summary contents
        try:
            table_summary = soup.find("summary").text
        except Exception:
            import traceback

            traceback.print_exc()
            table_summary = ""

        lines = content.split("\n")
        # Initialize an empty list to hold the parsed bullet points
        bullet_points = []
        # Loop through each line
        bullet_point_id = 1
        for line in lines:
            # If the line starts with '+', it is a bullet point
            if line.startswith("+"):
                # Remove the '+ ' from the start of the line and add it to the list
                bullet_points.append(f"{bullet_point_id}. " + line[1:].strip().strip('"'))
                bullet_point_id += 1
        return table_summary, "\n".join(bullet_points)


class ImageSummaryExecutor(DataSummaryExecutor):
    SUMMARY_PROMPT_TEMPLATE = """
{img_info}

Provide a succinct summary of the uploaded file with less than 20 words. Please ensure your summary is a complete sentence and include it within <summary></summary> tags. For image, just show its name is basically enough."
Then provide {num_insights} very simple and basic suggestions in natural language about further processing with the data. The suggestions should be able to be solved by python(e.g., grayscale, rescale, rotation, etc). The final results should be markdown '+' bullet point list, e.g., + The first suggestion."

Begin.
"""
    stream_handler = ExecutorStreamingChainHandler()

    def run(
        self,
        grounding_source: ImageDataModel,
        llm: BaseLanguageModel,
        use_intelligent_summary: bool = True,
        num_insights: int = 3,
    ) -> Dict[str, Any]:
        summary = ""
        if isinstance(grounding_source, ImageDataModel):
            # Basic summary
            raw_data = grounding_source.raw_data
            img_size, img_mode, img_format = raw_data["size"], raw_data["mode"], raw_data["format"]
            summary += f"Your image **{grounding_source.simple_filename}** is a {img_size[0]}x{img_size[1]} {img_mode} image in {img_format} format.\n"

            # Intelligent summary
            if use_intelligent_summary:
                intelligent_summary = self._intelligent_summary(
                    grounding_source,
                    num_insights=num_insights,
                    llm=llm,
                )
                _, suggestions = self._parse_output(intelligent_summary)
                summary += "\n" + "Here are some additional insights to enhance your understanding of the image"
                summary += "\n" + suggestions

            for stream_token in summary.split(" "):
                self.stream_handler.on_llm_new_token(stream_token)
        else:
            raise ValueError(f"Unsupported data summary for grounding source type: {type(grounding_source)}")
        return summary

    def _intelligent_summary(self, grounding_source: ImageDataModel, num_insights: int, llm: BaseLanguageModel) -> str:
        """Use LLM to generate data summary."""
        summary_prompt_template = PromptTemplate(
            input_variables=["img_info", "num_insights"],
            template=self.SUMMARY_PROMPT_TEMPLATE,
        )
        method = LLMChain(llm=llm, prompt=summary_prompt_template)
        result = method.run({"img_info": grounding_source.get_llm_side_data(), "num_insights": num_insights})
        return result

    def _parse_output(self, content: str) -> Tuple[str, str]:
        """Parse the output of the LLM to get the data summary."""
        from bs4 import BeautifulSoup

        # Using 'html.parser' to parse the content
        soup = BeautifulSoup(content, "html.parser")
        # Parsing the tag and summary contents
        try:
            table_summary = soup.find("summary").text
        except Exception:
            import traceback

            traceback.print_exc()
            table_summary = ""

        lines = content.split("\n")
        # Initialize an empty list to hold the parsed bullet points
        bullet_points = []
        # Loop through each line
        bullet_point_id = 1
        for line in lines:
            # If the line starts with '+', it is a bullet point
            if line.startswith("+"):
                # Remove the '+ ' from the start of the line and add it to the list
                bullet_points.append(f"{bullet_point_id}. " + line[1:].strip().strip('"'))
                bullet_point_id += 1
        return table_summary, "\n".join(bullet_points)
