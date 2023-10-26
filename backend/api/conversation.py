import struct
import json
import datetime
from typing import Any, Generator
from bson.objectid import ObjectId
from flask import jsonify, request, Response

from backend.app import app
from backend.utils.user_conversation_storage import get_user_conversation_storage
from backend.main import threading_pool, logger
from backend.schemas import DEFAULT_USER_ID
from backend.schemas import INTERNAL, UNFOUND


@app.route("/api/conversations/get_conversation_list", methods=["POST"])
def get_conversation_list() -> Response:
    """Gets the history conversations."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    conversations = []
    try:
        # Login with API Key, then retrieve the user history based
        # on the hashed API key.
        db = get_user_conversation_storage()
        conversation_list = db.conversation.find({"user_id": user_id})
        for conversation in conversation_list:
            conversations.append(
                {
                    "id": str(conversation["_id"]),
                    "name": conversation["name"],
                    "folderId": conversation["folder_id"],
                }
            )
    except Exception as e:
        return Response(response=None,
                        status=f'{INTERNAL} error fetch conversation list')
    return jsonify(conversations)


@app.route("/api/conversations/get_folder_list", methods=["POST"])
def get_folder_list() -> Response:
    """Gets the folder list."""
    user_id = DEFAULT_USER_ID
    folders = []
    try:
        db = get_user_conversation_storage()
        folder_list = db.folder.find({"user_id": user_id})
        for folder in folder_list:
            folders.append(
                {
                    "id": str(folder["_id"]),
                    "name": folder["name"],
                    "type": "chat",
                }
            )
        return jsonify({"success": True, "data": folders})
    except Exception as e:
        return Response(response=None, status=f'{INTERNAL} error fetch folder list')


def process_rich_content_item(data: dict, message_id: str) -> dict:
    """Processes the rich content from db format into frontend renderable format."""
    processed_items: dict = {"intermediateSteps": [], "finalAnswer": []}
    if "intermediate_steps" in data:
        for item in data["intermediate_steps"]:
            processed_items["intermediateSteps"].append(
                {"message_id": message_id, "content": item["text"],
                 "type": item["type"]}
            )
    if "final_answer" in data:
        for item in data["final_answer"]:
            processed_items["finalAnswer"].append(
                {"message_id": message_id, "content": item["text"],
                 "type": item["type"]}
            )
    return processed_items


@app.route("/api/conversation", methods=["POST"])
def get_conversation_content() -> Response:
    """Gets the conversation content for one assigned conversation."""
    request_json = request.get_json()
    conversation_id = request_json.get("chat_id", None)
    if conversation_id is not None:
        try:
            db = get_user_conversation_storage()
            conversation = db.conversation.find_one({"_id": ObjectId(conversation_id)})
            message_list = db.message.find({"conversation_id": conversation_id}).sort(
                "_id", -1)
            messages = [
                {
                    "id": message["message_id"],
                    "parent_message_id": message["parent_message_id"],
                    "role": message["role"],
                    "content": message["data_for_human"] if message[
                                                                "role"] == "user" else None,
                    "type": "rich_message" if isinstance(message["data_for_human"],
                                                         dict) else "",
                    "richContent": process_rich_content_item(message["data_for_human"],
                                                             message["message_id"])
                    if isinstance(message["data_for_human"], dict)
                    else None,
                }
                for message in message_list
            ]

            def _get_activated_conversation_branch(messages: list) -> list:
                # By default, the latest message is the end point, e.g., the current branch of messages.
                activated_messages: list = []
                end_point = messages[0]["id"]
                while len(messages) > 0 and end_point != -1:
                    flag = False
                    for msg in messages:
                        if msg["id"] == end_point:
                            if end_point == msg["parent_message_id"]:
                                flag = False
                                break
                            activated_messages = [msg] + activated_messages
                            end_point = msg["parent_message_id"]
                            flag = True
                            break
                    if not flag:
                        break
                return activated_messages

            # Find the current activated branch of messages as frontend only shows one branch

            if messages:
                messages = _get_activated_conversation_branch(messages)

            logger.bind(msg_head=f"get_activated_message_list").debug(messages)

            conversation = {
                "id": conversation_id,
                "name": conversation["name"],
                "messages": messages,
                "agent": conversation["agent"],
                "prompt": conversation["prompt"],
                "temperature": conversation["temperature"],
                "folderId": conversation["folder_id"],
                "bookmarkedMessagesIds": conversation["bookmarked_message_ids"],
                "selectedCodeInterpreterPlugins": conversation[
                    "selected_code_interpreter_plugins"],
                "selectedPlugins": conversation["selected_plugins"],

            }
            return jsonify(conversation)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(response=None,
                            status=f'{INTERNAL} error fetch conversation')
    else:
        return Response(response=None, status=f'{INTERNAL} error fetch conversation')


@app.route("/api/conversations/update_conversation", methods=["POST"])
def update_conversation() -> Response:
    """Updates a conversation name."""
    try:
        request_json = request.get_json()
        conversations = request_json["conversations"]
        db = get_user_conversation_storage()
        messages = []
        success = True
        update_key_dict = {"name": "name", "folder_id": "folderId"}
        for conversation_to_update in conversations:
            conversation_id = conversation_to_update["id"]
            name = conversation_to_update["name"]
            updates = {}
            for key in update_key_dict.keys():
                if update_key_dict[key] in conversation_to_update:
                    updates[key] = conversation_to_update[update_key_dict[key]]
            if conversation_id is not None:
                try:
                    db.conversation.update_one({"_id": ObjectId(conversation_id)},
                                               {"$set": updates})
                    messages.append("Conversation name updated to {}.".format(name))
                except Exception as e:
                    messages.append(str(e))
                    success = False
            else:
                success = False
                messages.append("Missing conversation id or title.")
        return jsonify({"success": success, "message": " ".join(messages)})
    except Exception as e:
        return Response(response=None, status=f"{INTERNAL} error fetch conversation")


@app.route("/api/conversations/update_folder", methods=["POST"])
def update_folder() -> Response:
    """Update a folder name."""
    request_json = request.get_json()
    folder_id = request_json["folder_id"]
    folder_name = request_json["name"]
    try:
        db = get_user_conversation_storage()
        db.folder.update_one({"_id": ObjectId(folder_id)},
                             {"$set": {"name": folder_name}})
        return jsonify({"success": True,
                        "message": "Folder name updated to {}.".format(folder_name)})
    except Exception as e:
        return Response(response=None, status=f"{INTERNAL} error update folder")


@app.route("/api/conversations/register_folder", methods=["POST"])
def register_folder() -> Response:
    """Creates a new folder."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    folder = request_json.get("folder", None)
    if folder:
        try:
            db = get_user_conversation_storage()
            folder = db.folder.insert_one({"name": folder["name"], "user_id": user_id})
            return jsonify({"id": str(folder.inserted_id),
                            "message": "Register folder successfully."})
        except Exception as e:
            return Response(response=None, status=f"{INTERNAL} error register folder")
    else:
        return Response(response=None, status=f"{UNFOUND} missing folder")


@app.route("/api/conversations/register_conversation", methods=["POST"])
def register_conversation() -> Response:
    """Creates a new conversation."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    conversation = request_json.get("conversation", None)
    if conversation:
        try:
            db = get_user_conversation_storage()
            conversation_id = conversation["id"]
            if conversation_id is not None and db.conversation.find_one(
                    {"_id": ObjectId(conversation_id)}):
                updates = {
                    "name": conversation["name"],
                    "agent": conversation["agent"],
                    "prompt": conversation["prompt"],
                    "temperature": conversation["temperature"],
                    "folder_id": conversation["folderId"],
                    "bookmarked_message_ids": conversation.get("bookmarkedMessagesIds",
                                                               None),
                    "selected_code_interpreter_plugins": conversation[
                        "selectedCodeInterpreterPlugins"],
                    "selected_plugins": conversation["selectedPlugins"],
                }
                db.conversation.update_one({"_id": ObjectId(conversation_id)},
                                           {"$set": updates})
            else:
                conversation = db.conversation.insert_one(
                    {
                        "name": conversation["name"],
                        "agent": conversation["agent"],
                        "prompt": conversation["prompt"],
                        "temperature": conversation["temperature"],
                        "folder_id": conversation["folderId"],
                        "bookmarked_message_ids": conversation.get(
                            "bookmarkedMessagesIds", None),
                        "hashed_api_key": "",
                        "user_id": user_id,
                        "selected_code_interpreter_plugins": conversation[
                            "selectedCodeInterpreterPlugins"],
                        "selected_plugins": conversation["selectedPlugins"],
                        "timestamp": datetime.datetime.utcnow(),
                    }
                )
                conversation_id = str(conversation.inserted_id)
            return jsonify({"id": conversation_id})
        except Exception as e:
            return Response(response=None,
                            status=f"{INTERNAL} error register conversation")
    else:
        return Response(response=None, status=f"{UNFOUND} missing conversation")


@app.route("/api/conversations/delete_conversation", methods=["POST"])
def delete_conversation() -> Response:
    """Deletes a conversation."""
    request_json = request.get_json()
    chat_id = request_json.get("chat_id", None)
    if chat_id:
        try:
            db = get_user_conversation_storage()
            db.conversation.delete_one({"_id": ObjectId(chat_id)})
            db.message.delete_many({"conversation_id": chat_id})
            return jsonify({"success": True, "message": "Conversation is deleted."})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    else:
        return jsonify({"success": False, "message": "chat_id is missing"})


@app.route("/api/conversations/delete_folder", methods=["POST"])
def delete_folder() -> Response:
    """Deletes a folder."""
    request_json = request.get_json()
    folder_id = request_json.get("folder_id", None)
    if folder_id:
        try:
            db = get_user_conversation_storage()
            db.folder.delete_one({"_id": ObjectId(folder_id)})
            return jsonify({"success": True, "message": "Folder is deleted."})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    else:
        return jsonify({"success": False, "message": "folder_id is missing"})


@app.route("/api/conversations/clear", methods=["POST"])
def clear_all_conversation() -> Response:
    """Clears all previous conversations."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    if user_id:
        try:
            db = get_user_conversation_storage()
            db.conversation.delete_many({"user_id": user_id})
            db.folder.delete_many({"user_id": user_id})
            db.message.delete_many({"user_id": user_id})
            return jsonify({"success": True, "message": "Clear All Conversations."})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    else:
        return jsonify({"success": False, "message": "user_id is missing"})


@app.route("/api/conversations/stop_conversation", methods=["POST"])
def stop_generation() -> Response:
    """Stops the current generation, cut on streaming."""
    try:
        request_json = request.get_json()
        chat_id = request_json["chat_id"]
        threading_pool.kill_thread(chat_id)
    except Exception as e:
        print(e)
        return Response(response={}, status=f"{INTERNAL} error stopping")

    def pack_json(object: Any) -> bytes:
        json_text = json.dumps(object)
        return struct.pack("<i", len(json_text)) + json_text.encode("utf-8")

    def yield_stop() -> Generator[bytes, Any, None]:
        yield pack_json({"success": False, "error": "stop"})

    return Response(response={})
