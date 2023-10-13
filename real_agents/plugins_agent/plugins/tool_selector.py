"""Implementation of Tool Selector that automate the selection of tools for the question (or sub-question)."""
import os
import pickle

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from typing import Any

from real_agents.adapters.data_model import SpecModel
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings

DEFAULT_TOOL_INSTRUCTION = "Represent the tool description for retrieval:"
DEFAULT_QUERY_INSTRUCTION = "Represent the question for retrieving tools that can be used to solve the question:"
PLUGIN_SPEC_FILE = "openapi.yaml"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
EMBEDDING_CACHE_PATH = os.path.join(CURRENT_PATH, "..", "..", "..", "backend", "static", "tool_embeddings")
if not os.path.exists(EMBEDDING_CACHE_PATH):
    os.makedirs(EMBEDDING_CACHE_PATH)


class ToolSelector:
    """
    This class is used to select the appropriate tool list for the question.
    """

    # add valid mode here if needed
    valid_modes = ["embedding"]

    """
    Example:
        .. code-block:: python
            mode_args = {"embedding": HuggingFaceInstructEmbeddings, "model_name": "hkunlp/instructor-large", "embed_instruction": "Represent the tool description for retrieval:", "query_instruction": "Represent the question for retrieving tools that can be used to solve the question:"}
            tool_selector = ToolSelector(mode="embedding", mode_args=mode_args)
            model_name = "hkunlp/instructor-large"
            model_kwargs = {'device': 'cpu'}
            hf = HuggingFaceInstructEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs
            )
    """
    user_id: str = None
    chat_id: str = None

    def __init__(self, tools_list: list = [], mode: str = "embedding", mode_args=None, api_key_pool: Any = None):
        """
        Initialize the tool selector.
        """
        if mode_args is None:
            mode_args = {}
        if mode not in self.valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Valid modes are {self.valid_modes}")
        self.tool_paths = [
            plugin_file_path
            for plugin_file_path in os.listdir(CURRENT_PATH)
            if ".py" not in plugin_file_path
               and plugin_file_path != "_scripts"
               and plugin_file_path != "__pycache__"
               and plugin_file_path != "README.md"
               and plugin_file_path != "descriptions.json"
        ]
        self.tool_list = tools_list
        self.mode = mode
        self.api_key_pool = api_key_pool
        if mode == "embedding":
            self._init_embedding(mode_args)
        else:
            raise ValueError(f"Unhandled mode '{mode}'.")

    def _init_embedding(self, mode_args: dict):
        embedding = mode_args.get("embedding", HuggingFaceInstructEmbeddings)
        if embedding == HuggingFaceInstructEmbeddings:
            model_name = mode_args.get("model_name", "hkunlp/instructor-large")
            embed_instruction = mode_args.get("embed_instruction", DEFAULT_TOOL_INSTRUCTION)
            query_instruction = mode_args.get("query_instruction", DEFAULT_QUERY_INSTRUCTION)
            self.embedding = HuggingFaceInstructEmbeddings(
                model_name=model_name, embed_instruction=embed_instruction, query_instruction=query_instruction
            )

    def get_tool_descriptions(self) -> list:
        """
        Get the tool descriptions.
        """
        descriptions = []
        tool_paths = self.tool_paths
        yaml_paths = [os.path.join(CURRENT_PATH, tool_name, PLUGIN_SPEC_FILE) for tool_name in tool_paths]
        for yaml_path, plugin_file_path in tqdm(zip(yaml_paths, tool_paths), total=len(yaml_paths)):
            if os.path.isdir(os.path.join(CURRENT_PATH, plugin_file_path)):
                retrieved = False
                try:
                    spec_model = SpecModel(yaml_path)
                    retrieved = True
                except:
                    print("Error loading yaml", yaml_path)
                if not retrieved:
                    description = "No description."
                else:
                    description = (
                        spec_model.full_spec["info"]["description"] if "description" in spec_model.full_spec[
                            "info"] else "No description."
                    )
                descriptions.append(description)
        return descriptions

    def get_api_key_from_tool_name(self, tool_name: str) -> str:
        """
        Get the API key from the tool name.
        """
        user_id = self.user_id
        api_key_info = self.api_key_pool.get_pool_info_with_id(user_id, default_value=[])
        if len([i for i in api_key_info if i["tool_name"] == tool_name]) != 0:
            api_key = [i for i in api_key_info if i["tool_name"] == tool_name][0]["api_key"]
        else:
            api_key = None
        return api_key

    def check_plugin_valid(self, tool_path: str) -> bool:
        """
        Check if the plugin is valid. Return false if this plugin requires an API key but the user has not provided one or plugin not found.
        """
        plugins = self.tool_list
        # check if plugin exists and get the plugin if it exists
        if len([i for i in plugins if i["name"].lower() == tool_path.lower()]) != 0:
            plugin = [i for i in plugins if i["name"].lower() == tool_path.lower()][0]
        else:
            plugin = None
            print(f"Plugin {tool_path} not found.")

        # check if plugin requires an API key and if the user has provided one
        if plugin is not None:
            if plugin["require_api_key"] and self.get_api_key_from_tool_name(tool_path) == None:
                return False
            else:
                return True
        else:
            return False

    def load_query_from_message_list(self, message_list: list[dict[str, str]], user_intent: str) -> str:
        """
        Load the query from the message list.
        """

        """
        Example:
        message_list = [{'message_type': 'human_message', 'message_content': 'buy nike shoes', 'message_id': 362, 'parent_message_id': -1}, {'message_type': 'ai_message', 'message_content': '', 'message_id': 363, 'parent_message_id': 362}]
        """
        # concatenate all history messages into one single query
        # The message_list is the history message list so we need to concatenate user intent(current message) to the end of the message list
        query = ""
        for message in message_list:
            # only concatenate human messages since we only need to retrieve tools based on user intent and the ai_message can be long sometimes which will influence the embedding
            if "message_content" in message.keys() and "message_type" in message.keys() and message[
                "message_type"] == 'human_message':
                query += (message["message_content"] + " ")
            else:
                continue
        query += user_intent
        return query

    def select_tools(self, query: str = "", top_k: int = 8):
        """
        Select the top k tools based on the similarity between the query and the tool description.
        """
        if query == "":
            raise ValueError("Query cannot be empty.")
        if self.mode not in self.valid_modes:
            raise ValueError(f"Invalid mode '{self.mode}'. Valid modes are {self.valid_modes}")

        if self.mode == "embedding":
            return self._select_tools_embedding(query, top_k)
        else:
            raise ValueError(f"Unhandled mode '{self.mode}'.")

    def _select_tools_embedding(self, query: str, top_k: int) -> list[str]:
        embedding = self.embedding
        # check if the embedding is InstructorEmbeddings
        if isinstance(self.embedding, HuggingFaceInstructEmbeddings):
            tool_embeddings = []
            for name, description in zip(self.tool_paths, self.get_tool_descriptions()):
                # Define file path for the cached embedding
                tool_embedding_file = EMBEDDING_CACHE_PATH + "/" + name + ".pkl"
                # Check if tool embedding is already cached
                if os.path.isfile(tool_embedding_file):
                    with open(tool_embedding_file, "rb") as f:
                        tool_embedding = pickle.load(f)
                # no cached embedding, compute and cache it
                else:
                    tool_embedding = embedding.embed_documents([description])
                    with open(tool_embedding_file, "wb") as f:
                        pickle.dump(tool_embedding, f)
                tool_embeddings.extend(tool_embedding)

            query_embeddings = [embedding.embed_query(query)]

            similarities = cosine_similarity(query_embeddings, tool_embeddings)

            # eliminate invalid plugins
            for idx, tool_path in enumerate(self.tool_paths):
                if not self.check_plugin_valid(tool_path):
                    similarities[0][idx] = -1

            # get indices of top k similarities
            top_k_indices = np.argsort(similarities.flatten())[-top_k:]

            top_k_indices = top_k_indices.tolist()

            # return upper case tool names since tool id is the upper case of its name
            return [tool_name.upper() for idx, tool_name in enumerate(self.tool_paths) if idx in top_k_indices]
