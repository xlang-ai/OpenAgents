import redis
from typing import Any

from backend.utils.utils import logger
import os

r = redis.Redis(host=os.getenv("REDIS_SERVER"), port=6379, decode_responses=True)


# Set the queue and pending key
QUEUE_RUNNING = "kernel_running_queue"
QUEUE_PENDING = "kernel_pending_queue"
SUBMIT_EVENT = "job_submitted"
RUNNING_EVENT = "job_started"
COMPLETE_EVENT = "job_completed"

MAX_CONCURRENT_KERNELS = 300


def add_job_to_pending(job: Any) -> None:
    # always add the jobn to pending
    r.rpush(QUEUE_PENDING, job)


def move_pending_to_running() -> None:
    """Move pending jobs to the running queue."""
    # Get the first pending job
    job = r.lindex(QUEUE_PENDING, 0)
    if job is not None:
        logger.bind(msg_head="Job running").debug(job)
        # Move the job from pending queue to running queue
        r.rpush(QUEUE_RUNNING, job)
        # Notify the running channel
        r.publish(RUNNING_EVENT, job)
        # Remove the job from pending queue
        r.lpop(QUEUE_PENDING)


# Subscribe to job completion events
def handle_job_completion(message: dict) -> None:
    # the data should be the chat id
    chat_id = message["data"]
    logger.bind(msg_head="Job completed").debug(chat_id)
    # here we only care about the capacity, not caring about which one is poped now
    logger.bind(msg_head="Queue running").debug(r.lrange(QUEUE_RUNNING, 0, -1))
    r.lrem(QUEUE_RUNNING, 0, chat_id)
    move_pending_to_running()


def handle_new_job(message: dict) -> None:
    # the data should be the chat id
    chat_id = message["data"]
    logger.bind(msg_head="Job submitted").debug(chat_id)
    # all submitted jobs into pending queue
    add_job_to_pending(chat_id)
    # push the id to the pending queue
    logger.bind(msg_head="Queue pending").debug(r.lrange(QUEUE_PENDING, 0, -1))
    if r.llen(QUEUE_RUNNING) < MAX_CONCURRENT_KERNELS:
        move_pending_to_running()


def start_kernel_publisher() -> None:
    # Connect to Redis
    r.delete(QUEUE_RUNNING)
    r.delete(QUEUE_PENDING)
    # Start the publisher & subscriber
    p = r.pubsub()
    p.subscribe(**{COMPLETE_EVENT: handle_job_completion, SUBMIT_EVENT: handle_new_job})

    p.run_in_thread(sleep_time=0.1)
