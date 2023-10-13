import json
import os
import re
import shutil
import uuid
from typing import Any, Dict, List, Tuple
import requests
from bs4 import BeautifulSoup
from loguru import logger
from kaggle.api.kaggle_api_extended import KaggleApi

from langchain.base_language import BaseLanguageModel
from langchain import PromptTemplate

from real_agents.adapters.llm import LLMChain


class KaggleDataLoadingExecutor:
    KAGGLE_TEMPLATE = """

Determine whether the user input aims to (1) connect to a specific kaggle dataset that the user mentions its kaggle path
(2) search for relevant kaggle datasets given the information the user provides.

You need to output the action wrapped in <action></action>, the action space is ['connect', 'search']. You also need
to output the keywords wrapped in <keywords></keywords>. For 'search', the keywords MUST be ONE search term/word to be
searched by kaggle api. Note keywords CAN'T be too specific or contain trivial word(e.g., dataset), make sure there are various search results. For
'connect', the keywords are the kaggle dataset path.

Input: {input}

Begin."
"""

    def run(
        self,
        user_intent: str,
        llm: BaseLanguageModel,
        search_top_k: int = 4,
    ) -> Dict[str, Any]:
        logger.bind(msg_head="KaggleDataLoader inputs").trace(user_intent)
        kaggle_template = PromptTemplate(
            input_variables=["input"],
            template=self.KAGGLE_TEMPLATE,
        )
        method = LLMChain(llm=llm, prompt=kaggle_template)
        result = method.run({"input": user_intent})
        logger.bind(msg_head="LLM result").trace(result)
        kaggle_action, keywords = self._parse_output(result)
        logger.bind(msg_head="Kaggle action").trace(kaggle_action)
        logger.bind(msg_head="Kaggle keywords").trace(keywords)
        """Use export to manage the Kaggle API key for now."""
        api = KaggleApi()
        api.authenticate()
        if kaggle_action == "connect":
            kaggle_output_info = keywords
        elif kaggle_action == "search":
            kaggle_output_info = self._search_kaggle(api, keywords, search_top_k)
        else:
            # Regard the rest as "search" action now
            kaggle_action = "search"
            kaggle_output_info = self._search_kaggle(api, keywords, search_top_k)
        return {"kaggle_action": kaggle_action, "kaggle_output_info": kaggle_output_info}

    def _search_kaggle(self, api: KaggleApi, keywords: str, search_top_k: int) -> List[Dict]:
        """Search kaggle datasets given the keywords."""
        # Search for datasets
        datasets = []
        for page in range(1, 10):
            try:
                searched_datasets = api.dataset_list(search=keywords, page=page, max_size=20000, file_type="csv")

                logger.bind(msg_head="Kaggle search result").trace(searched_datasets)

                datasets.extend(searched_datasets)
                if len(datasets) >= search_top_k:
                    datasets = datasets[:search_top_k]
                    break
                if len(searched_datasets) < 20:
                    # Default page_size is 20, less than 20 means no more datasets can be searched
                    break
            except Exception:
                break

        # Get url, cover image and some meta data for each dataset
        if len(datasets) == 0:
            # No datasets found
            datasets = api.dataset_list(max_size=20000, page=1, file_type="csv")[:search_top_k]

        output_info = self._get_dataset_meta_info(api, datasets)
        return output_info

    def _get_dataset_meta_info(self, api: KaggleApi, datasets: List) -> List[Dict]:
        """Get dataset key meta-data to be shown to the user."""
        output_info = []
        for dataset in datasets:
            dataset_hash_id = str(uuid.uuid4())
            dataset_tmp_dir = os.path.join(".kaggle_meta/", dataset_hash_id)
            os.makedirs(dataset_tmp_dir, exist_ok=True)
            api.dataset_metadata(dataset.ref, path=dataset_tmp_dir)
            with open(os.path.join(dataset_tmp_dir, "dataset-metadata.json")) as f:
                dataset_metadata = json.load(f)
            shutil.rmtree(os.path.join(".kaggle_meta/", dataset_hash_id))
            dataset_url = "https://www.kaggle.com/datasets/" + dataset.ref
            # Crawling the dataset page to get the dataset image
            dataset_cover_image_url = self._crawl_dataset_cover_image(dataset_url)

            logger.bind(msg_head="Dataset cover image url").trace(dataset_cover_image_url)

            output_metadata = {
                "id": dataset_metadata["id"],
                "id_no": dataset_metadata["id_no"],
                "title": dataset_metadata["title"],
                "subtitle": dataset_metadata["subtitle"],
                "total_views": dataset_metadata["totalViews"],
                "total_votes": dataset_metadata["totalVotes"],
                "total_downloads": dataset_metadata["totalDownloads"],
                "url": dataset_url,
                "cover_image_url": dataset_cover_image_url,
            }
            output_info.append(output_metadata)
        return output_info

    def _crawl_dataset_cover_image(
        self, url: str, default_image_path="https://images.datacamp.com/image/upload/v1647430873/kaggle_logo_icon_168474_4eb653edb6.png"
    ) -> str:
        """Crawl the kaggle dataset cover image from the dataset url."""
        # Get the HTML content of the webpage
        response = requests.get(url)

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the image element
        try:
            kaggle_component_element = soup.find("script", {"class": "kaggle-component"})
            match = re.search(r'"coverImageUrl":\s*"([^"]*)"', kaggle_component_element.string)
            image_url = match.group(1)
        except Exception:
            import traceback

            traceback.print_exc()
            image_url = default_image_path

        return image_url

    def _parse_output(self, content: str) -> Tuple[str, str]:
        """Parse the output of the LLM to get the kaggle action and keywords."""
        from bs4 import BeautifulSoup

        # Using 'html.parser' to parse the content
        soup = BeautifulSoup(content, "html.parser")
        # Parsing the tag and summary contents
        try:
            action = soup.find("action").text
        except Exception:
            action = ""

        try:
            keywords = soup.find("keywords").text
        except Exception:
            keywords = ""

        return action, keywords
