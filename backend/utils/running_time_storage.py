import redis
from flask import g
import os


def get_running_time_storage():
    """Connects to redis."""
    if "running_time_storage" not in g:
        g.running_time_storage = redis.Redis(host=os.getenv("REDIS_SERVER"), port=6379, decode_responses=True)
        # Set maxmemory to 200MB (value is in bytes)
        g.running_time_storage.config_set("maxmemory", "500000000")
        # Set maxmemory policy to allkeys-lru (Least Recently Used)
        g.running_time_storage.config_set("maxmemory-policy", "allkeys-lru")
    return g.running_time_storage
