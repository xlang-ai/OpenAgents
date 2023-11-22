import base64
import copy
import json
import os
import random
import traceback
from typing import Dict, List, Union

import requests
from flask import Response, request, stream_with_context
from retrying import retry

from backend.api.language_model import get_llm
from backend.app import app
from backend.main import message_id_register, message_pool, logger
from backend.utils.streaming import single_round_chat_with_agent_streaming
from backend.schemas import OVERLOAD, NEED_CONTINUE_MODEL, DEFAULT_USER_ID
from backend.main import api_key_pool
from real_agents.adapters.llm import BaseLanguageModel
from real_agents.adapters.agent_helpers import AgentExecutor, Tool
from real_agents.adapters.callbacks.agent_streaming import \
    AgentStreamingStdOutCallbackHandler
from real_agents.adapters.data_model import DataModel, JsonDataModel
from real_agents.adapters.interactive_executor import initialize_plugin_agent
from real_agents.adapters.memory import ConversationReActBufferMemory
from real_agents.plugins_agent.plugins.utils import load_all_plugins_elements
from real_agents.plugins_agent.plugins.tool_selector import ToolSelector
from real_agents.plugins_agent import PluginExecutor

# The plugins list
global plugins
plugins = []

# Set up the tool selector for automatically selecting plugins
try:
    tool_selector = ToolSelector(tools_list=plugins, mode="embedding", api_key_pool=api_key_pool)
except Exception as e:
    print(e, "The auto selection feature of plugins agent will return random elements.")
    tool_selector = None

# Load plugin info and icon image
for plugin_type, plugin_info in load_all_plugins_elements().items():
    @retry(stop_max_attempt_number=10,
           wait_fixed=2000)  # Retry 3 times with a 2-second delay between retries
    def make_request(_image_url) -> Response:
        response = requests.get(_image_url)  # Replace with your actual request code
        response.raise_for_status()  # Raise an exception for unsuccessful response status codes
        return response


    # Load icon image
    image_url = plugin_info["meta_info"]["manifest"]["logo_url"]

    # If image is base64 encoded
    if image_url.startswith("data:image"):
        plugins.append(
            {
                "id": plugin_type,
                "name": plugin_type,
                "name_for_human": plugin_info["meta_info"]["manifest"][
                    "name_for_human"],
                "description": plugin_info["description"],
                "icon": image_url,
                "require_api_key": plugin_info["need_auth"],
            }
        )
        continue

    image_format = image_url.split(".")[-1]

    try:
        # Check if in cache
        os.makedirs("backend/static/images", exist_ok=True)
        if os.path.exists(f"backend/static/images/{plugin_type}.cache"):
            with open(f"backend/static/images/{plugin_type}.cache", "rb") as f:
                image_content = f.read()
        else:
            response = make_request(image_url)
            image_content = response.content
            # Make a .cache file for the image
            with open(f"backend/static/images/{plugin_type}.cache", "wb") as f:
                f.write(image_content)
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to make the request {plugin_type}:", e)
        continue

    if image_format == "svg":
        encoded_image = "data:image/svg+xml;base64,  ".format(
            image_format) + base64.b64encode(image_content).decode(
            "utf-8"
        )
    else:
        encoded_image = "data:image/{};base64,  ".format(
            image_format) + base64.b64encode(image_content).decode(
            "utf-8"
        )

    plugins.append(
        {
            "id": plugin_type,
            "name": plugin_type,
            "name_for_human": plugin_info["meta_info"]["manifest"]["name_for_human"],
            "description": plugin_info["description"],
            "icon": encoded_image,
            "require_api_key": plugin_info["need_auth"],
        }
    )


def create_plugins_interaction_executor(
        selected_plugins: List[str],
        api_key_info: List[Dict],
        llm: BaseLanguageModel,
        llm_name: str,
) -> AgentExecutor:
    """Creates an agent executor for interaction.

    Args:
        selected_plugins: A list of selected plugins.
        api_key_info: A list of plugin api keys.
        llm: A llm model.
        llm_name: A string llm name.

    Returns:
        An agent executor.

    """
    # Initialize memory
    memory = ConversationReActBufferMemory(memory_key="chat_history",
                                           return_messages=True, style="plugin",
                                           max_token_limit=10000)

    class RunPlugin:
        def __init__(self, plugin: PluginExecutor, llm: BaseLanguageModel):
            self.plugin = plugin
            self.llm = llm

        def run(self, term: str) -> Union[str, Dict, DataModel]:
            try:
                raw_observation = self.plugin.run(user_intent=term, llm=self.llm)
                input_json, output = raw_observation["input_json"], raw_observation[
                    "api_output"]
                observation = JsonDataModel.from_raw_data(
                    {
                        "success": True,
                        "result": json.dumps(output, indent=4) if isinstance(output,
                                                                             dict) else output,
                        "intermediate_steps": json.dumps(input_json, indent=4),
                    }
                )
                return observation

            except Exception as e:
                observation = JsonDataModel.from_raw_data(
                    {
                        "success": False,
                        "result": str(e),
                    }
                )
                print(traceback.format_exc())
                return observation

    # Load plugins from selected names
    _plugins = []
    for selected_plugin in selected_plugins:
        plugin = PluginExecutor.from_plugin_name(selected_plugin)
        llm = copy.deepcopy(llm)

        if len([i for i in api_key_info if i["tool_name"] == plugin.name]) != 0:
            plugin.api_key = \
            [i for i in api_key_info if i["tool_name"] == plugin.name][0]["api_key"]
            # For some plugins, we need to reload the plugin to update personal data
            plugin.load_personnel_info()  # warning: this will change the plugin object every time we make a new query

        run_plugin = RunPlugin(plugin, llm)

        _plugins.append(Tool(name=plugin.name, func=run_plugin.run,
                             description=plugin.full_description))

    continue_model = llm_name if llm_name in NEED_CONTINUE_MODEL else None
    interaction_executor = initialize_plugin_agent(
        _plugins, llm, continue_model, memory=memory, verbose=True
    )

    return interaction_executor


@app.route("/api/chat_xlang_plugin", methods=["POST"])
def chat_xlang_plugin() -> Dict:
    """Returns the chat response of plugins agent."""
    try:
        # Get request parameters
        request_json = request.get_json()
        user_id = request_json.pop("user_id", DEFAULT_USER_ID)
        chat_id = request_json["chat_id"]
        user_intent = request_json["user_intent"]
        parent_message_id = request_json["parent_message_id"]
        selected_plugins = request_json["selected_plugins"]
        llm_name = request_json["llm_name"]
        temperature = request_json.get("temperature", 0.4)
        stop_words = ["[RESPONSE_BEGIN]", "TOOL RESPONSE"]
        kwargs = {
            "temperature": temperature,
            "stop": stop_words,
        }

        # pass user id and chat id to tool selector
        if tool_selector:
            tool_selector.user_id = user_id
            tool_selector.chat_id = chat_id

        # Get language model
        llm = get_llm(llm_name, **kwargs)

        logger.bind(user_id=user_id, chat_id=chat_id, api="/chat",
                    msg_head="Request json").debug(request_json)

        # Get API key for plugins
        api_key_info = api_key_pool.get_pool_info_with_id(user_id,
                                                          default_value=[])  # fixme: mock user_id: 1

        activated_message_list = message_pool.get_activated_message_list(user_id,
                                                                         chat_id,
                                                                         list(),
                                                                         parent_message_id)

        # Flag for auto retrieving plugins
        if len(selected_plugins) == 1 and selected_plugins[0].lower() == "auto":

            if tool_selector:
                # this will return a list of plugin names sorted by relevance (lower case and the same as their dir name)
                query = tool_selector.load_query_from_message_list(activated_message_list,
                                                                   user_intent)
                selected_plugins = tool_selector.select_tools(query=query, top_k=5)
            else:
                selected_plugins = [_plugin['id'] for _plugin in random.sample(plugins, 5)]

        # Build executor and run chat
        stream_handler = AgentStreamingStdOutCallbackHandler()
        interaction_executor = create_plugins_interaction_executor(
            selected_plugins=selected_plugins,
            api_key_info=api_key_info,
            llm=llm,
            llm_name=llm_name,
        )

        message_pool.load_agent_memory_from_list(interaction_executor.memory,
                                                 activated_message_list)

        human_message_id = message_id_register.add_variable(user_intent)
        ai_message_id = message_id_register.add_variable("")

        return stream_with_context(
            Response(
                single_round_chat_with_agent_streaming(
                    interaction_executor=interaction_executor,
                    user_intent=user_intent,
                    human_message_id=human_message_id,
                    ai_message_id=ai_message_id,
                    user_id=user_id,
                    chat_id=chat_id,
                    message_list=activated_message_list,
                    parent_message_id=parent_message_id,
                    stream_handler=stream_handler,
                    llm_name=llm_name,
                    app_type="plugins",
                ),
                content_type="application/json",
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return Response(response=None,
                        status=f"{OVERLOAD} backend is currently overloaded")
