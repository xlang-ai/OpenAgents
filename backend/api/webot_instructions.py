from flask import request, jsonify, Response

from backend.main import app
from backend.schemas import DEFAULT_USER_ID
from backend.api.chat_webot import get_webot_from_redis, \
    get_webot_status_from_redis, reset_webot_status


@app.route("/api/webot/instructions", methods=["POST"])
def get_instruction() -> Response:
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
    return jsonify({
        "chat_id": chat_id,
        "user_id": user_id,
        "instructions": webot.instruction
    })


@app.route("/api/webot/webot_status", methods=["POST"])
def get_webot_status() -> Response:
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    webot_status_json = get_webot_status_from_redis(user_id=user_id, chat_id=chat_id)
    return jsonify(webot_status_json) if webot_status_json is not None else jsonify(
        {"webot_status": None, "url": None})


@app.route("/api/webot/reset_status", methods=["POST"])
def reset_status() -> Response:
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    reset_webot_status(user_id=user_id, chat_id=chat_id)
    return jsonify({
        "chat_id": chat_id,
        "user_id": user_id,
    })
