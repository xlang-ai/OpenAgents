from langchain.chat_models.google_palm import ChatGooglePalm

from real_agents.adapters.models.anthropic import ChatAnthropic
from real_agents.adapters.models.openai import ChatOpenAI

__all__ = [
    "ChatOpenAI",
    "ChatAnthropic",
    "ChatGooglePalm",
]

type_to_cls_dict = {
    "chat_anthropic": ChatAnthropic,
    "chat_google_palm": ChatGooglePalm,
    "chat_openai": ChatOpenAI,
}
