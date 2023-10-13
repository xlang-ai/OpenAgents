from typing import Dict
from flask import request, jsonify, Response

from backend.main import message_pool
from backend.app import app
from backend.api.language_model import get_llm
from backend.utils.utils import get_user_and_chat_id_from_request_json
from real_agents.adapters.executors import QuestionSuggestionExecutor
from real_agents.adapters.memory import ConversationReActBufferMemory


@app.route("/api/recommend", methods=["POST"])
def recommend() -> dict | Response:
    """Recommends potential inputs for users. """
    try:
        request_json = request.get_json()
        (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
        parent_message_id = int(request_json["parent_message_id"])
        user_intent = request_json["user_intent"]

        # Find the mainstat message list from leaf to root
        activated_message_list = message_pool.get_activated_message_list(
            user_id, chat_id, default_value=list(), parent_message_id=parent_message_id
        )
        chat_memory = ConversationReActBufferMemory(memory_key="chat_history", return_messages=True)
        message_pool.load_agent_memory_from_list(chat_memory, activated_message_list)
        question_suggestion_executor = QuestionSuggestionExecutor()
        
        llm_name = request_json["llm_name"]
        temperature = request_json.get("temperature", 0.7)
        kwargs = {
            "temperature": temperature,
        }

        # Get language model
        llm = get_llm(llm_name, **kwargs)
        follow_questions = question_suggestion_executor.run(
            user_intent=user_intent,
            llm=llm,
            chat_memory=chat_memory,
            mode="chat_memory",
        )

        return jsonify({
            "recommend_questions": follow_questions["questions"], 
            "user_id": user_id,
            "chat_id": chat_id,
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "recommend_questions": [],
            "user_id": user_id,
            "chat_id": chat_id,
        }
