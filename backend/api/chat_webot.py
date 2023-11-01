from time import sleep
import copy
import redis
import json
import pickle
import traceback
from flask import Response, request, stream_with_context
from typing import Dict, Union
import os

from langchain.schema import HumanMessage, SystemMessage

from backend.api.language_model import get_llm
from backend.main import app, message_id_register, message_pool, logger
from backend.utils.streaming import single_round_chat_with_agent_streaming
from backend.schemas import OVERLOAD, NEED_CONTINUE_MODEL
from backend.schemas import DEFAULT_USER_ID
from real_agents.adapters.llm import BaseLanguageModel
from real_agents.adapters.agent_helpers import AgentExecutor, Tool
from real_agents.adapters.callbacks.agent_streaming import \
    AgentStreamingStdOutCallbackHandler
from real_agents.adapters.models import ChatOpenAI
from real_agents.adapters.memory import ConversationReActBufferMemory
from real_agents.adapters.data_model import DataModel, JsonDataModel
from real_agents.adapters.interactive_executor import initialize_webot_agent
from real_agents.web_agent import WebBrowsingExecutor, WebotExecutor

r = redis.Redis(host=os.getenv("REDIS_SERVER"), port=6379, db=0)  # adjust host/port/db as needed


# here webot and webot_status are stored in redis since the two global variable can not be modified and accessed normally in multiprocess
# fixme:now webot is stored without message_id or chat_id info, so it can only be used for one chat at a time
# fixme:now webot_status is stored with chat_id info, if the status is not reset after a message ended abnormally e.g. the message is interrupted, it will be reused wrongly for the next chat
def get_webot_from_redis(user_id: str, chat_id: str, ) -> WebBrowsingExecutor:
    data = r.get(f'webot_{user_id}_{chat_id}')
    if data is not None:
        webot = pickle.loads(data)
    else:
        # initialize a webot with None instrucition if webot does not exist
        webot = WebBrowsingExecutor(None)
        save_webot_to_redis(user_id, chat_id, webot)
    return webot


def save_webot_to_redis(user_id: str, chat_id: str, webot: WebBrowsingExecutor, ):
    r.set(f'webot_{user_id}_{chat_id}', pickle.dumps(webot))


def get_webot_status_from_redis(user_id: str, chat_id: str):
    webot_status_json = r.get(f'webot_status_{user_id}_{chat_id}')
    if webot_status_json is not None:
        webot_status = json.loads(webot_status_json)
        return webot_status
    else:
        return {}


def save_webot_status_to_redis(user_id: str, chat_id: str, webot_status: Dict):
    r.set(f'webot_status_{user_id}_{chat_id}', json.dumps(webot_status))


def reset_webot(user_id: str, chat_id: str):
    webot = WebBrowsingExecutor(None)
    save_webot_to_redis(user_id, chat_id, webot)


def reset_webot_status(user_id: str, chat_id: str):
    webot_status = {"webot_status": "idle", "url": None}
    save_webot_status_to_redis(user_id, chat_id, webot_status)


# this function has been deprecated
def get_plan(instruction: str, start_url: str, chat_llm: ChatOpenAI):
    # fixme: Move this into a separate chain or executors to decompose the LLMs
    system_message = f"""
You are a planner to assist another browser automation assistant.

Here is the instruction for the other assistant:
```
You MUST take one of the following actions. NEVER EVER EVER make up actions that do not exist:

1. click(element): Clicks on an element
2. setValue(element, value: string): Focuses on and sets the value of an input element
3. finish(): Indicates the task is finished
4. fail(): Indicates that you are unable to complete the task
You will be be given a task to perform and the current state of the DOM. You will also be given previous actions that you have taken. You may retry a failed action up to one time.

This is an example of an action:

<Thought>I should click the add to cart button</Thought>
<Action>click(223)</Action>

You MUST always include the <Thought> and <Action> open/close tags or else your response will be marked as invalid.

Rules you MUST follow:
1. You must only take one step at a time. You cannot take multiple actions in a single response.
2. You should not consider the action to present the result to the user. You only need to do available actions. If info in current page is enough for the user to solve the problem, you should finish.
```
Now your responsibility is to give a step-by-step plan according to user's instruction. This plan will be given to the assistant as a reference when it is performing tasks.
""".strip()

    human_message = f"""
The user requests the following task:

{instruction}

Now you are at {start_url}

Provide a plan to do this (you can use pseudo description as below to describe the item).

Here is an example case:

request: Go to google calendar to schedule a meeting

current url: "https://google.com"

example plan:

1. setValue(searchBar, "google calendar")
2. click(search)
3. click(the item with title of google calendar)
4.1 if user has loginned 
    do nothing 
4.2 if user hasn't loginned 
    do login 
5. click(create event button) 
6. setValue(event title input bar, "meeting") 
7. click(save event button)
8. finish()
""".strip()

    messages = [SystemMessage(content=system_message),
                HumanMessage(content=human_message)]
    response = chat_llm(messages).content
    return response


def create_webot_interaction_executor(
        llm: BaseLanguageModel,
        llm_name: str,
        user_id: str,
        chat_id: str
) -> AgentExecutor:
    """Creates an agent executor for interaction.

    Args:
        llm: A llm model.
        llm_name: A string llm name.
        user_id: A string of user id.
        chat_id: A string chat id.

    Returns:
        An agent executor.

    """
    # Initialize memory
    memory = ConversationReActBufferMemory(memory_key="chat_history",
                                           return_messages=True, max_token_limit=10000)

    class RunWebot:
        def __init__(self, webot: WebotExecutor, llm: BaseLanguageModel, user_id: str,
                     chat_id: str):
            self.llm = llm
            self.webot = webot
            self.user_id = user_id
            self.chat_id = chat_id

        def run(self, term: str) -> Union[str, Dict, DataModel]:
            try:
                user_id = self.user_id
                chat_id = self.chat_id
                reset_webot(user_id=user_id, chat_id=chat_id)
                reset_webot_status(user_id=user_id, chat_id=chat_id)
                raw_observation = self.webot.run(user_intent=term, llm=self.llm)
                instruction, start_url = raw_observation["instruction"], \
                    raw_observation["start_url"]
                webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
                webot.instruction = instruction
                # webot.plan = get_plan(instruction, start_url)
                webot.plan = ""
                save_webot_to_redis(user_id=user_id, chat_id=chat_id, webot=webot)
                webot_status = {
                    "webot_status": "running",
                    "url": start_url
                }
                save_webot_status_to_redis(user_id=user_id, chat_id=chat_id,
                                           webot_status=webot_status)
                while True:
                    webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
                    if webot.finish or webot.interrupt or webot.error or webot.fail:
                        break
                    else:
                        sleep(0.5)
                save_webot_status_to_redis(user_id=user_id, chat_id=chat_id,
                                           webot_status={"webot_status": "idle",
                                                         "url": None})
                webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
                webot.instruction = None
                save_webot_to_redis(user_id=user_id, chat_id=chat_id, webot=webot)

                if webot.finish:
                    webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
                    action_history = webot.action_history
                    last_page = webot.pages_viewed[-1]
                    observation = JsonDataModel.from_raw_data(
                        {
                            "success": True,
                            "result": json.dumps({"action_history": action_history,
                                                  "last_page": last_page}, indent=4),
                            "intermediate_steps": json.dumps(
                                {"instruction": instruction, "start_url": start_url},
                                indent=4)
                        }
                    )
                    return observation

                if webot.fail:
                    observation = JsonDataModel.from_raw_data(
                        {
                            "success": True,
                            "result": "The webot failed to execute the instruction.",
                            "intermediate_steps": json.dumps(
                                {"instruction": instruction, "start_url": start_url},
                                indent=4)
                        }
                    )
                    return observation

                if webot.interrupt:
                    observation = JsonDataModel.from_raw_data(
                        {
                            "success": False,
                            "result": "The web browsing is interrupted by user.",
                            "intermediate_steps": json.dumps(
                                {"instruction": instruction, "start_url": start_url},
                                indent=4)
                        }
                    )
                    return observation

                if webot.error:
                    observation = JsonDataModel.from_raw_data(
                        {
                            "success": False,
                            "result": "Error occurs during web browsing.",
                            "intermediate_steps": json.dumps(
                                {"instruction": instruction, "start_url": start_url},
                                indent=4)
                        }
                    )
                    return observation

            except Exception as e:
                print(traceback.format_exc())
                observation = JsonDataModel.from_raw_data(
                    {
                        "success": False,
                        "result": f"Failed in web browsing with the input: {term}, please try again later.",
                        "intermediate_steps": json.dumps({"error": str(e)})
                    }
                )
                return observation

    webot = WebotExecutor.from_webot()
    llm = copy.deepcopy(llm)
    run_webot = RunWebot(webot, llm, chat_id=chat_id, user_id=user_id)
    tools = [Tool(name=webot.name, func=run_webot.run, description=webot.description)]

    continue_model = llm_name if llm_name in NEED_CONTINUE_MODEL else None
    interaction_executor = initialize_webot_agent(
        tools, llm, continue_model, memory=memory, verbose=True
    )
    return interaction_executor


@app.route("/api/chat_xlang_webot", methods=["POST"])
def chat_xlang_webot() -> Dict:
    """Returns the chat response of web agent."""
    try:
        # Get request parameters
        request_json = request.get_json()
        user_id = request_json.pop("user_id", DEFAULT_USER_ID)
        chat_id = request_json["chat_id"]
        user_intent = request_json["user_intent"]
        parent_message_id = request_json["parent_message_id"]
        llm_name = request_json["llm_name"]
        temperature = request_json.get("temperature", 0.4)
        stop_words = ["[RESPONSE_BEGIN]", "TOOL RESPONSE"]
        kwargs = {
            "temperature": temperature,
            "stop": stop_words,
        }

        # Get language model
        llm = get_llm(llm_name, **kwargs)

        logger.bind(user_id=user_id, chat_id=chat_id, api="/chat",
                    msg_head="Request json").debug(request_json)

        human_message_id = message_id_register.add_variable(user_intent)
        ai_message_id = message_id_register.add_variable("")

        stream_handler = AgentStreamingStdOutCallbackHandler()
        # Build executor and run chat

        # reset webot and status
        reset_webot(user_id=user_id, chat_id=chat_id)
        reset_webot_status(user_id=user_id, chat_id=chat_id)

        interaction_executor = create_webot_interaction_executor(
            llm=llm,
            llm_name=llm_name,
            chat_id=chat_id,
            user_id=user_id
        )

        activated_message_list = message_pool.get_activated_message_list(user_id,
                                                                         chat_id,
                                                                         list(),
                                                                         parent_message_id)
        message_pool.load_agent_memory_from_list(interaction_executor.memory,
                                                 activated_message_list)
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
                    app_type="webot",
                ),
                content_type="application/json",
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return Response(response=None,
                        status=f"{OVERLOAD} backend is currently overloaded")
