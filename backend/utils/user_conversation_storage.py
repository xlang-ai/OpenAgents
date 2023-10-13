import pymongo
from flask import g


def get_user_conversation_storage():
    """Connects to mongodb."""
    if "user_conversation_storage" not in g:
        g.user_conversation_storage = pymongo.MongoClient("mongodb://localhost:27017/")
    return g.user_conversation_storage["xlang"]


def close_user_conversation_storage():
    """Closes mongodb."""
    user_conversation_storage = g.pop("user_conversation_storage", None)
    if user_conversation_storage is not None:
        user_conversation_storage["xlang"].close()
