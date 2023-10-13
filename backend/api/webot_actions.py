from flask import request, jsonify, Response

from backend.api.chat_webot import get_webot_from_redis, save_webot_to_redis
from backend.main import app
from backend.schemas import DEFAULT_USER_ID
from backend.api.language_model import get_llm


@app.route("/api/webot/action", methods=["POST"])
def get_action() -> Response:
    """Gets the next action to take for a given the current page HTML."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
    # Get request parameters
    request_json = request.get_json()
    processed_html = request_json["processed_html"]
    llm = get_llm("gpt-4")
    result = webot.run(processed_html, llm=llm)
    save_webot_to_redis(user_id=user_id, chat_id=chat_id, webot=webot)

    return jsonify({
        "chat_id": chat_id,
        "user_id": user_id,
        "action_response": result,
    })


@app.route("/api/webot/interrupt", methods=["POST"])
def interrupt() -> Response:
    """Interrupts the current webot."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    interrupt = request_json["interrupt"]
    if interrupt:
        webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
        webot.actions_taken.append("interrupt")
        save_webot_to_redis(user_id=user_id, chat_id=chat_id, webot=webot)
        return jsonify({
            "chat_id": chat_id,
            "user_id": user_id,
        })
    return jsonify({"message": "No interrupt signal received."})


@app.route("/api/webot/error", methods=["POST"])
def error() -> Response:
    """Appends action 'error' to the current webot."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    error = request_json["error"]
    if error:
        webot = get_webot_from_redis(user_id=user_id, chat_id=chat_id)
        webot.actions_taken.append("error")
        save_webot_to_redis(user_id=user_id, chat_id=chat_id, webot=webot)
        return jsonify({
            "chat_id": chat_id,
            "user_id": user_id,
        })
    return jsonify({"message": "No error signal received."})
