from typing import Any, Dict

from langchain.base_language import BaseLanguageModel
from langchain.schema import AIMessage, HumanMessage

from real_agents.adapters.memory import ConversationReActBufferMemory
from real_agents.adapters.executors.question_suggestion.chat_memory import QuestionSuggestionChainChatMemory
from real_agents.adapters.executors.question_suggestion.base import QuestionSuggestionChainBase
from real_agents.adapters.executors.question_suggestion.user_profile import QuestionSuggestionChainUserProfile


class QuestionSuggestionExecutor:
    def run(
        self,
        user_intent: str,
        llm: BaseLanguageModel,
        num_questions: int = 3,
        mode: str = "",
        user_profile: str = "",
        chat_memory: ConversationReActBufferMemory = ConversationReActBufferMemory(),
    ) -> Dict[str, Any]:
        if mode == "base":
            method = QuestionSuggestionChainBase.from_prompt(llm)
            inputs = {"input_string": user_intent, "num_questions": num_questions}
        elif mode == "user_profile":
            method = QuestionSuggestionChainUserProfile.from_prompt(llm)
            with open(user_profile) as f:
                inputs = {"input_string": user_intent, "num_questions": num_questions, "user_description": f.read()}
        elif mode == "chat_memory":
            method = QuestionSuggestionChainChatMemory.from_prompt(llm)
            raw_history = chat_memory.load_memory_variables({})["chat_history"]
            refine_history = []
            for msg in raw_history[-4:]:
                if isinstance(msg, HumanMessage):
                    refine_history.append(f"Human: {msg.content}")
                elif isinstance(msg, AIMessage):
                    refine_history.append(f"AI: {msg.content}")
            inputs = {
                "input_string": user_intent,
                "num_questions": num_questions,
                "chat_memory": "\n".join(refine_history),
            }
        else:
            raise ValueError(f"Mode {mode} is not supported")
        return method(inputs)
