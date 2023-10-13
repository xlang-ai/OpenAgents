from typing import Dict, List, Type

from langchain.schema import BaseMemory
from langchain.memory.chat_memory import BaseChatMemory

from real_agents.adapters.memory.buffer import (
    ConversationBufferMemory,
    ConversationStringBufferMemory,
)
from real_agents.adapters.memory.read_only_string_memory import ReadOnlySharedStringMemory
from real_agents.adapters.memory.buffer import ConversationReActBufferMemory



__all__ = [
    "ConversationBufferMemory",
    "ConversationReActBufferMemory",
    "ConversationStringBufferMemory",
    "BaseMemory",
    "BaseChatMemory",
    "ReadOnlySharedStringMemory",
]

type_to_cls_dict: Dict[str, Type[BaseMemory]] = {
    "chat_buffer": ConversationBufferMemory,
    "chat_string_buffer": ConversationStringBufferMemory,
}
