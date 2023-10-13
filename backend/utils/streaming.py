import json
import re
import struct
import time
from typing import Any, Dict, List, Optional, Literal
import multiprocess
import requests
from bs4 import BeautifulSoup

from backend.display_streaming import DisplayStream
from backend.main import logger, message_pool, threading_pool
from backend.utils.user_conversation_storage import get_user_conversation_storage
from backend.utils.utils import error_rendering
from backend.memory import MessageMemoryManager
from backend.schemas import (
    APP_TYPES,
    TIME_OUT_MAP,
    HEARTBEAT_INTERVAL,
    STREAM_BLOCK_TYPES,
    STREAM_TOKEN_TYPES,
    EXECUTION_RESULT_MAX_TOKENS_MAP,
)
from real_agents.data_agent import DataSummaryExecutor
from real_agents.adapters.callbacks.agent_streaming import AgentStreamingStdOutCallbackHandler
from real_agents.adapters.agent_helpers import Agent, AgentExecutor
from real_agents.adapters.llm import BaseLanguageModel


def check_url_exist(text: str) -> bool:
    """check in a text whether there is a url"""
    # this regex extracts the http(s) with whitespace or () in the beginning and end, since usually the url is surrounded by whitespace or ()
    # e.g. " https://google.com " or "(https://google.com)"
    url_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"

    links = re.findall(url_regex, text)
    return len(links) > 0


# function to extract links from text
def extract_links(text: str) -> list[Any]:
    url_regex = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"
    links = re.findall(url_regex, text)
    return links


# function to extract image links from a webpage
def extract_title_and_image_links(url: str) -> (tuple[Literal[''], list] | tuple[Any, list]):
    try:
        res = requests.get(url, timeout=3)
        if res.status_code != 200:
            return "", []
        soup = BeautifulSoup(res.text, "html.parser")
        title_tag = soup.find_all("title")[0].text
        img_tags = soup.find_all("img")
        # List to store image links with large width and height
        large_img_links = []
        # List to store all image links
        all_img_links = []
        for img in img_tags:
            if "src" in img.attrs:
                all_img_links.append(img["src"])
                # Check if width and height attributes exist and add to the large list
                if "width" in img.attrs and "height" in img.attrs:
                    # Ensure the width and height attributes can be converted to integers
                    if int(img["width"]) > 100 and int(img["height"]) > 100:
                        large_img_links.append(img["src"])
                    else:
                        continue
        # If large images were found, return those, otherwise return all images
        img_links = large_img_links if large_img_links else []
        # fixme: handle the case there are no such tags

        return title_tag, img_links
    except requests.exceptions.Timeout:
        print("Request timed out!")
        return "", []
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return "", []


def extract_card_info_from_text(message: str) -> list:
    links = extract_links(message)
    rt = []
    for link in links:
        title, image_links = extract_title_and_image_links(link)
        if len(image_links) > 0:
            selected_image_link = image_links[0]
        else:
            selected_image_link = ""  # no image in this website
        rt.append({"title": title, "web_link": link, "image_link": selected_image_link})
    return rt


def extract_card_info_from_links(links: List[str]) -> list[dict[str, Any]]:
    rt = []
    for link in links:
        if check_url_exist(link):
            title, image_links = extract_title_and_image_links(link)
            if len(image_links) > 0:
                selected_image_link = image_links[0]
            else:
                selected_image_link = ""  # no image in this website
            rt.append({"title": title, "web_link": link, "image_link": selected_image_link})
        else:
            continue
    return rt


def pack_json(object: Any) -> bytes:
    json_text = json.dumps(object)
    return struct.pack("<i", len(json_text)) + json_text.encode("utf-8")


def _streaming_block(
    fancy_block: Dict,
    is_final: bool,
    user_id: str,
    chat_id: str,
) -> bytes:
    """Stream a block to the frontend."""
    render_position = "intermediate_steps" if not is_final else "final_answer"
    return pack_json(
        {
            render_position: [
                {
                    "type": fancy_block["type"],
                    "text": fancy_block["text"],
                }
            ],
            "is_block_first": True,
            "streaming_method": "block",
            "user_id": user_id,
            "chat_id": chat_id,
        }
    )


def _streaming_token(token: Dict, is_final: bool, user_id: str, chat_id: str, is_block_first: bool) -> bytes:
    """Streams a token to the frontend."""
    render_position = "intermediate_steps" if not is_final else "final_answer"
    return pack_json(
        {
            render_position: {
                "type": token["type"],
                "text": token["text"],
            },
            "is_block_first": is_block_first,
            "streaming_method": "char",
            "user_id": user_id,
            "chat_id": chat_id,
        }
    )


def _wrap_agent_caller(
    interaction_executor: Any,
    inputs: Dict[str, Any],
    chat_id: str,
    err_pool: Dict[str, Any],
    memory_pool: Dict[str, Any],
    callbacks: List,
) -> None:
    try:
        _ = interaction_executor(inputs, callbacks=callbacks)
        message_list_from_memory = MessageMemoryManager.save_agent_memory_to_list(interaction_executor.memory)
        memory_pool.update({chat_id: message_list_from_memory})
        del interaction_executor
    except Exception as e:
        import traceback

        traceback.print_exc()

        err_pool[chat_id] = f"{type(e).__name__}: {str(e)}"


def _combine_streaming(stream_list: List) -> List:
    """Combine the streaming tokens/blocks to be saved in database."""
    stream_list_combined = []
    current_type, current_text = None, ""
    for idx, item in enumerate(stream_list):
        if current_type in STREAM_TOKEN_TYPES and (item["type"] != current_type) or idx == len(stream_list) - 1:
            stream_list_combined.append(
                {
                    "type": current_type,
                    "text": current_text,
                }
            )
            current_text = ""
        if item["type"] in STREAM_BLOCK_TYPES:
            stream_list_combined.append(item)
        elif item["type"] in STREAM_TOKEN_TYPES:
            current_text += item["text"]
        current_type = item["type"]
    return stream_list_combined


def _render_preprocess(string: Optional[str] = None) -> str:
    """Preprocess the string to be rendered in frontend."""
    if string is None:  # this is due to openai stop policy or other stream issue
        return ""
    string = string.replace("$", "\$")
    return string


def single_round_chat_with_agent_streaming(
    stream_handler: AgentStreamingStdOutCallbackHandler,
    interaction_executor: AgentExecutor,
    user_intent: str,
    human_message_id: int,
    ai_message_id: int,
    user_id: str,
    chat_id: str,
    message_list: List[Dict[str, Any]],
    parent_message_id: int,
    llm_name: str,
    app_type: str = "plugins",
) -> Any:
    """Streams the response of the agent to the frontend."""
    assert app_type in APP_TYPES, f"app_type should be one of {APP_TYPES}"

    with multiprocess.Manager() as share_manager:
        err_pool: Dict[str, Any] = share_manager.dict()
        memory_pool: Dict[str, Any] = share_manager.dict()
        share_list = share_manager.list()
        memory_pool[chat_id] = []

        stream_handler.for_display = share_list

        chat_thread = multiprocess.Process(
            target=_wrap_agent_caller,
            args=(
                interaction_executor,
                {
                    "input": user_intent,
                },
                chat_id,
                err_pool,
                memory_pool,
                [stream_handler],
            ),
        )

        threading_pool.register_thread(chat_id, chat_thread)
        chat_thread.start()
        empty_s_time: float = -1
        last_heartbeat_time: float = -1
        timeout = TIME_OUT_MAP[app_type]
        LEFT_SIGN = "("
        RIGHT_SIGN = ")"
        start_buffer = False
        streamed_transition_text_buffer = ""
        streamed_links = []
        converted_card_info_list = []
        yield pack_json(
            {
                "human_message_id": human_message_id,
                "ai_message_id": ai_message_id,
            }
        )
        # Display streaming to frontend
        display_stream = DisplayStream(execution_result_max_tokens=EXECUTION_RESULT_MAX_TOKENS_MAP[app_type])
        is_block_first, current_block_type = False, None
        intermediate_list, final_list = [], []  # Only for database storage
        try:
            while chat_thread.is_alive() or len(stream_handler.for_display) > 0:
                # print(memory_pool, err_pool, "out")
                if stream_handler.is_end:
                    # The ending of the streaming is marked by the is_end variable from AgentStreamingStdOutCallbackHandler in agent_streaming.py
                    break

                if len(stream_handler.for_display) == 0:
                    # first time display list is empty
                    if empty_s_time == -1:
                        empty_s_time = time.time()
                    # already empty for some time
                    else:
                        if time.time() - empty_s_time > timeout and chat_thread.is_alive():
                            threading_pool.timeout_thread(chat_id)
                            break

                    if last_heartbeat_time == -1:
                        last_heartbeat_time = time.time()
                    else:
                        if time.time() - last_heartbeat_time > HEARTBEAT_INTERVAL and chat_thread.is_alive():
                            last_heartbeat_time = -1
                            yield _streaming_token(
                                {"text": "🫀", "type": "heartbeat", "final": False}, False, user_id, chat_id, False
                            )

                else:
                    empty_s_time = -1
                    last_heartbeat_time = -1

                while len(stream_handler.for_display) > 0:
                    token = stream_handler.for_display.pop(0)
                    items_to_display = display_stream.display(token)

                    # Skip the "identifier" and "key" token
                    if items_to_display is None:
                        continue

                    for item in items_to_display:
                        # Check if the block type is changed
                        if item["type"] != current_block_type:
                            current_block_type = item["type"]
                            is_block_first = True
                        else:
                            is_block_first = False
                        is_final = item.get("final", False)

                        # Render the item(s)
                        if item["type"] in STREAM_BLOCK_TYPES:
                            # Render image and echarts as block
                            yield _streaming_block(item, is_final, user_id, chat_id)
                        elif item["type"] in STREAM_TOKEN_TYPES:
                            # Render the rest as plain text
                            item["text"] = _render_preprocess(item["text"])
                            yield _streaming_token(item, is_final, user_id, chat_id, is_block_first)
                        # Save the intermediate steps and final answer
                        if is_final:
                            final_list.append(item)
                        else:
                            intermediate_list.append(item)

                        if item["type"] == "transition" and item["text"] == RIGHT_SIGN:
                            start_buffer = False
                            link = streamed_transition_text_buffer
                            streamed_transition_text_buffer = ""
                            card_info_list = extract_card_info_from_text(link)
                            # empty the buffer after extracting card info
                            streamed_transition_text_buffer = ""
                            if len(card_info_list) > 0:
                                streaming_card_info_list: list[dict[str, Any]] = [
                                    {
                                        "final_answer": {
                                            "text": json.dumps(card_info),
                                            "type": "card_info",
                                        },
                                        "is_block_first": False,
                                        "streaming_method": "card_info",
                                        "user_id": user_id,
                                        "chat_id": chat_id,
                                    }
                                    for card_info in card_info_list
                                ]
                                streamed_links.extend([card_info["web_link"] for card_info in card_info_list])
                                converted_card_info_list.extend(
                                    [
                                        {
                                            "text": stream_card_info["final_answer"]["text"],
                                            "type": stream_card_info["final_answer"]["type"],
                                        }
                                        for stream_card_info in streaming_card_info_list
                                    ]
                                )
                                for streaming_card_info in streaming_card_info_list:
                                    yield pack_json(streaming_card_info)

                        if start_buffer == True:
                            streamed_transition_text_buffer += item["text"]

                        if item["type"] == "transition" and item["text"] == LEFT_SIGN:
                            start_buffer = True

        except Exception as e:
            import traceback

            traceback.print_exc()
        # Wait for the chat thread to finish
        chat_thread.join()
        stop_flag, timeout_flag, error_msg = threading_pool.flush_thread(chat_id)
        error_msg = err_pool.pop(chat_id, None)
        # Response Error!!
        if stop_flag:
            yield pack_json({"success": False, "error": "stop"})
            return
        elif timeout_flag:
            yield pack_json({"success": False, "error": "timeout"})
            return
        elif error_msg is not None:
            error_msg_to_render = error_rendering(error_msg)
            yield pack_json({"success": False, "error": "internal", "error_msg": error_msg_to_render})
            return
        elif len(memory_pool[chat_id]) == 0:
            yield pack_json({"success": False, "error": "internal"})
            return
        # Response Success!!
        message_list_from_memory = memory_pool[chat_id]
        del stream_handler
        # share_manager.shutdown()
        del memory_pool, err_pool, share_list, share_manager, interaction_executor

    # Save conversation to memory
    new_human_message = message_list_from_memory[-2]
    new_ai_message = message_list_from_memory[-1]
    new_human_message.update({"message_id": human_message_id, "parent_message_id": parent_message_id})
    new_ai_message.update({"message_id": ai_message_id, "parent_message_id": human_message_id})
    message_list.extend([new_human_message, new_ai_message])

    logger.bind(user_id=user_id, chat_id=chat_id, api="/chat", msg_head="New human message").debug(new_human_message)
    logger.bind(user_id=user_id, chat_id=chat_id, api="/chat", msg_head="New ai message").debug(new_ai_message)

    MessageMemoryManager.set_pool_info_with_id(message_pool, user_id, chat_id, message_list)

    # Save conversation to database
    db = get_user_conversation_storage()
    # Combine the streaming tokens/blocks
    intermediate_list_combined = _combine_streaming(intermediate_list)
    final_list_combined = _combine_streaming(final_list)
    if len(converted_card_info_list) > 0:
        final_list_combined.extend(converted_card_info_list)
    # Insert User Message, if regenerate there is no need to insert again
    db.message.insert_one(
        {
            "conversation_id": chat_id,
            "user_id": user_id,
            "message_id": human_message_id,
            "parent_message_id": parent_message_id,
            "version_id": 0,
            "role": "user",
            "data_for_human": user_intent,
            "data_for_llm": message_list[-2]["message_content"],
            "raw_data": None,
        }
    )
    # Insert AI Message
    db.message.insert_one(
        {
            "conversation_id": chat_id,
            "user_id": user_id,
            "message_id": ai_message_id,
            "parent_message_id": human_message_id,
            "version_id": 0,
            "role": "assistant",
            "data_for_human": {
                "intermediate_steps": intermediate_list_combined,
                "final_answer": final_list_combined,
            },
            "data_for_llm": message_list[-1]["message_content"],
            "raw_data": None,
        }
    )


def _wrap_executor_caller(
    executor: Any, inputs: Any, llm: Any, chat_id: str, err_pool: Dict[str, Any], memory_pool: Dict[str, Any]
) -> None:
    try:
        results = executor.run(inputs, llm)
        message_list_from_memory = results
        memory_pool.update({chat_id: message_list_from_memory})
    except Exception as e:
        import traceback

        traceback.print_exc()

        err_pool[chat_id] = f"{type(e).__name__}: {str(e)}"


def single_round_chat_with_executor(
    executor: Any,
    user_intent: Any,
    human_message_id: int,
    ai_message_id: int,
    user_id: str,
    chat_id: str,
    message_list: List[Dict[str, Any]],
    parent_message_id: int,
    llm: BaseLanguageModel,
    app_type: str = "copilot",
) -> Any:
    """Streams the response of the executor to the frontend."""
    stream_handler = executor.stream_handler
    share_manager = multiprocess.Manager()
    err_pool: Dict[str, Any] = share_manager.dict()
    memory_pool: Dict[str, Any] = share_manager.dict()
    share_list = share_manager.list()
    stream_handler._all = share_list
    memory_pool[chat_id] = []
    chat_thread = multiprocess.Process(
        target=_wrap_executor_caller,
        args=(
            executor,
            user_intent,
            llm,
            chat_id,
            err_pool,
            memory_pool,
        ),
    )
    threading_pool.register_thread(chat_id, chat_thread)

    empty_s_time: float = -1
    timeout = TIME_OUT_MAP[app_type]
    chat_thread.start()
    yield pack_json(
        {
            "human_message_id": human_message_id,
            "ai_message_id": ai_message_id,
        }
    )
    # FIXME: treat data summary as a special tool
    STREAM_TOOL_TYPE = "tool"
    data_summary_tool_item = {
        "text": executor.tool_name,
        "type": STREAM_TOOL_TYPE,
    }
    yield _streaming_block(data_summary_tool_item, is_final=False, user_id=user_id, chat_id=chat_id)
    is_block_first = True
    final_answer = []
    while chat_thread.is_alive() or len(stream_handler._all) > 0:
        if stream_handler.is_end:
            break
        if len(stream_handler._all) == 0:
            # first time display list is empty
            if empty_s_time == -1:
                empty_s_time = time.time()
            # already empty for some time
            else:
                if time.time() - empty_s_time > timeout and chat_thread.is_alive():
                    threading_pool.timeout_thread(chat_id)
                    break
        else:
            empty_s_time = -1

        while len(stream_handler._all) > 0:
            text = stream_handler._all.pop(0)
            final_answer.append(text)
            if is_block_first:
                is_block_first_ = True
                is_block_first = False
            else:
                is_block_first_ = False
            yield pack_json(
                {
                    "final_answer": {
                        "type": "text",
                        "text": text + " ",
                    },
                    "is_block_first": is_block_first_,
                    "streaming_method": "char",
                    "user_id": user_id,
                    "chat_id": chat_id,
                }
            )
            time.sleep(0.035)
    chat_thread.join()
    stop_flag, timeout_flag, error_msg = threading_pool.flush_thread(chat_id)
    error_msg = err_pool.pop(chat_id, None)
    if stop_flag:
        yield pack_json({"success": False, "error": "stop"})
        return
    elif timeout_flag:
        yield pack_json({"success": False, "error": "timeout"})
        return
    elif error_msg is not None:
        error_msg_to_render = error_rendering(error_msg)
        yield pack_json({"success": False, "error": "internal", "error_msg": error_msg_to_render})
        return
    elif len(memory_pool[chat_id]) == 0 or len(final_answer) == 0:
        yield pack_json({"success": False, "error": "internal"})
        return
    # Response Success!!
    del share_list, stream_handler
    del memory_pool, err_pool, share_manager, executor

    # Save conversation to memory
    final_answer_str = " ".join(final_answer)
    message_list.append(
        {
            "message_id": ai_message_id,
            "parent_message_id": parent_message_id,
            "message_type": "ai_message",
            "message_content": final_answer_str,
        }
    )
    logger.bind(user_id=user_id, chat_id=chat_id, api="chat/", msg_head="New data summary message").debug(
        message_list[-1]
    )

    MessageMemoryManager.set_pool_info_with_id(message_pool, user_id, chat_id, message_list)

    # Database Operations
    db = get_user_conversation_storage()
    db.message.insert_one(
        {
            "conversation_id": chat_id,
            "user_id": user_id,
            "message_id": ai_message_id,
            "parent_message_id": parent_message_id,
            "version_id": 0,
            "role": "assistant",
            "data_for_human": {
                "intermediate_steps": [
                    data_summary_tool_item,
                ],
                "final_answer": [
                    {
                        "text": final_answer,
                        "type": "plain",
                    }
                ],
            },
            "data_for_llm": message_list[-1]["message_content"],
            "raw_data": None,
        }
    )
