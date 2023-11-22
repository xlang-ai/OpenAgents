from typing import Any, Dict, List, Union
from loguru import logger
import json

from backend.app import app
from backend.utils.running_time_storage import get_running_time_storage
from backend.utils.user_conversation_storage import get_user_conversation_storage
from real_agents.adapters.memory import BaseChatMemory

HUMAN_MESSAGE_KEY = "human_message"
AI_MESSAGE_KEY = "ai_message"

LOCAL = "local"
DATABASE = "database"


class UserMemoryManager:
    """A class to manage the global memory including messages, grounding_sources,
    etc. on user level"""

    # api_key_pool:
    # {
    #   "user_id": [{
    #       "tool_id": the id of the tool,
    #       "tool_name": the name of the tool,
    #       "api_key": the api_key of the tool,
    # }]
    # }

    def __init__(self, name: str = None, backend: str = LOCAL, memory_pool: Dict = None):
        self.backend = backend
        self.name = name
        if self.backend == LOCAL:
            if memory_pool is None:
                memory_pool = {}
            self.memory_pool = memory_pool
        elif self.backend == DATABASE:
            with app.app_context():
                self.redis_client = get_running_time_storage()
                self.db_client = get_user_conversation_storage()
        else:
            raise ValueError("Unknown backend option: {}".format(self.backend))

    def get_pool_info_with_id(
        self,
        user_id: str,
        default_value: Union[List, Dict],
    ) -> Any:
        """Gets the information with user_id and chat_id from the pool."""
        if self.backend == LOCAL:
            pool = self.memory_pool
            if user_id in pool:
                return pool[user_id]
            else:
                return default_value
        elif self.backend == DATABASE:
            memory_pool_name = f"{self.name}:{user_id}"
            if self.redis_client.exists(memory_pool_name):
                # In cache
                info = json.loads(self.redis_client.get(memory_pool_name))
            else:
                # Cache miss
                try:
                    # api_keys are not stored in database
                    if self.name == "api_key_pool":
                        info = default_value
                    else:
                        raise NotImplementedError(f"Currently only support message pool in database, not {self.name}")
                except Exception as e:
                    # Not in database
                    logger.bind(user_id=user_id, msg_head="Cache miss but not in database").warning(
                        "Failed to get pool info from database: {}".format(e)
                    )
                    info = default_value
            return info

    def set_pool_info_with_id(self, user_id: str, info: Any) -> None:
        """Sets the information with user_id and chat_id to the pool."""
        if self.backend == LOCAL:
            pool = self.memory_pool
            if user_id not in pool:
                pool[user_id] = info
        elif self.backend == DATABASE:
            # As db has its own updating logic, we only need to update the cache here (write-through).
            memory_pool_name = f"{self.name}:{user_id}"
            self.redis_client.set(memory_pool_name, json.dumps(info))

    def __iter__(self):
        """Iterates over the memory pool."""
        if self.backend == LOCAL:
            for user_id, info in self.memory_pool.items():
                yield user_id, info
        elif self.backend == DATABASE:
            raise NotImplementedError("Currently not support UserMemoryManager iteration in database mode.")


class ChatMemoryManager:
    """A class to manage the global memory including messages, grounding_sources, etc. on chat level"""

    # memory_pool:
    # {user_id: {chat_id: [
    #                           {"message_id": the id of this pair of messages,
    #                            "parent_message_id": the id of the parent message,
    #                            "message_type": type of the message, possible values: human_message / ai_message
    #                            "message_content": content of the message
    #                           }
    #                     ]
    #           }
    # }
    # grounding_source_pool:
    # {user_id: {chat_id: {"filenames": List of filenames,
    #                      "activated_filenames": List of user-selected activated names}}

    def __init__(self, name: str = None, backend: str = LOCAL, memory_pool: Dict = None):
        """
        This ChatMemoryManager can not be applied to grounding_source_pool in database mode.
        """
        self.backend = backend
        self.name = name
        if self.backend == LOCAL:
            if memory_pool is None:
                memory_pool = {}
            self.memory_pool = memory_pool
        elif self.backend == DATABASE:
            with app.app_context():
                self.redis_client = get_running_time_storage()
                self.db_client = get_user_conversation_storage()
        else:
            raise ValueError("Unknown backend option: {}".format(self.backend))

    def get_pool_info_with_id(
        self,
        user_id: str,
        chat_id: str,
        default_value: Union[List, Dict],
    ) -> Any:
        """Gets the information with user_id and chat_id from the pool."""
        if self.backend == LOCAL:
            pool = self.memory_pool
            if user_id in pool and chat_id in pool[user_id]:
                return pool[user_id][chat_id]
            else:
                return default_value
        elif self.backend == DATABASE:
            memory_pool_name = f"{self.name}:{user_id}:{chat_id}"
            if self.redis_client.exists(memory_pool_name):
                # In cache
                info = json.loads(self.redis_client.get(memory_pool_name))
            else:
                # Cache miss
                try:
                    # Found in database
                    if self.name == "message_pool":
                        info = []
                        response = self.db_client.message.find({"conversation_id": chat_id})
                        if response is None:
                            # Not in database (new chat)
                            info = default_value
                        else:
                            # In database
                            for message in response:
                                if message["role"] == "user":
                                    message_type = HUMAN_MESSAGE_KEY
                                elif message["role"] == "assistant":
                                    message_type = AI_MESSAGE_KEY
                                else:
                                    raise ValueError("Unknown role: {}".format(message["role"]))
                                info.append(
                                    {
                                        "message_id": message["message_id"],
                                        "parent_message_id": message["parent_message_id"],
                                        "message_type": message_type,
                                        "message_content": message["data_for_llm"],
                                    }
                                )
                            self.redis_client.set(memory_pool_name, json.dumps(info))
                    elif self.name == "jupyter_kernel_pool":
                        info = default_value
                    else:
                        raise NotImplementedError(f"Currently only support message pool in database, not {self.name}")
                except Exception as e:
                    # Not in database
                    logger.bind(user_id=user_id, chat_id=chat_id, msg_head="Cache miss but not in database").warning(
                        "Failed to get pool info from database: {}".format(e)
                    )
                    info = default_value
            return info

    def set_pool_info_with_id(self, user_id: str, chat_id: str, info: Any) -> None:
        """Sets the information with user_id and chat_id to the pool."""
        if self.backend == LOCAL:
            pool = self.memory_pool
            if user_id not in pool:
                pool[user_id] = {}
            pool[user_id][chat_id] = info
        elif self.backend == DATABASE:
            # As db has its own updating logic, we only need to update the cache here (write-through).
            memory_pool_name = f"{self.name}:{user_id}:{chat_id}"
            self.redis_client.set(memory_pool_name, json.dumps(info))

    def __iter__(self):
        """Iterates over the memory pool."""
        if self.backend == LOCAL:
            for user_id, chat_id_info in self.memory_pool.items():
                for chat_id, info in chat_id_info.items():
                    yield user_id, chat_id, info
        elif self.backend == DATABASE:
            if self.name == "jupyter_kernel_pool":
                iterator = self.redis_client.scan_iter("jupyter_kernel_pool:*")
                for key in iterator:
                    user_id, chat_id = key.split(":")[1:]
                    yield user_id, chat_id, self.get_pool_info_with_id(user_id, chat_id, {})
            else:
                raise NotImplementedError("Currently only support jupyter kernel pool iteration in database mode.")

    def drop_item_with_id(self, user_id: str, chat_id: str):
        if self.backend == LOCAL:
            # drop item under one user
            if user_id in self.memory_pool:
                self.memory_pool[user_id].pop([chat_id], None)
        elif self.backend == DATABASE:
            if self.name == "jupyter_kernel_pool":
                self.redis_client.delete(f"{self.name}:{user_id}:{chat_id}")
            else:
                raise NotImplementedError("Currently only support jupyter kernel pool delete in database mode.")


class MessageMemoryManager(ChatMemoryManager):
    """A class to manage the memory of messages."""

    @staticmethod
    def load_agent_memory_from_list(agent_memory: BaseChatMemory, message_list: List[Dict[str, str]]) -> None:
        """Load agent's memory from a list."""
        agent_memory.clear()
        for message in message_list:
            if message.get("message_type", None) == HUMAN_MESSAGE_KEY:
                agent_memory.chat_memory.add_user_message(message["message_content"])
            elif message.get("message_type", None) == AI_MESSAGE_KEY:
                agent_memory.chat_memory.add_ai_message(message["message_content"])
        try:
            agent_memory.fit_max_token_limit()
        except Exception as e:
            import traceback

            traceback.print_exc()
            pass

    @staticmethod
    def save_agent_memory_to_list(agent_memory: BaseChatMemory) -> List[Dict[str, str]]:
        """Saves agent's memory to a list"""
        messages = agent_memory.chat_memory.messages
        message_list = []
        for message in messages:
            if message.type == "human":
                message_list.append(
                    {
                        "message_type": "human_message",
                        "message_content": message.content,
                    }
                )
            elif message.type == "ai":
                message_list.append(
                    {
                        "message_type": "ai_message",
                        "message_content": message.content,
                    }
                )
        return message_list

    def get_activated_message_list(
        self,
        user_id: str,
        chat_id: str,
        default_value: Union[List, Dict],
        parent_message_id: Union[int, str],
    ) -> List:
        """Gets the activated message list from leaf to root."""
        # ONLY work for messages
        message_list = self.get_pool_info_with_id(user_id, chat_id, default_value)
        activated_message_list = []
        end_point = parent_message_id
        while len(message_list) > 0 and end_point != -1:
            flag = False
            for msg in message_list:
                if msg["message_id"] == end_point:
                    if end_point == msg["parent_message_id"]:
                        flag = False
                        break
                    activated_message_list = [msg] + activated_message_list
                    end_point = msg["parent_message_id"]
                    flag = True
                    break
            if not flag:
                break
        logger.bind(msg_head=f"get_activated_message_list").debug(activated_message_list)
        return activated_message_list
