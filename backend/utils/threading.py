# Python program using
# traces to kill threads
from typing import Dict, Tuple, Optional
from multiprocess import Process


class ThreadManager:
    """Manager class of all user chat threads."""

    def __init__(self) -> None:
        self.thread_pool: Dict[str, Process] = {}
        self.stop_pool: Dict[str, bool] = {}
        self.timeout_pool: Dict[str, bool] = {}
        self.run_error_pool: Dict[str, Optional[str]] = {}

    def register_thread(self, chat_id, thread: Process) -> None:
        self.thread_pool[chat_id] = thread
        self.stop_pool[chat_id] = False
        self.timeout_pool[chat_id] = False
        self.run_error_pool[chat_id] = None

    def flush_thread(self, chat_id) -> Tuple[bool, bool, str]:
        # self.thread_pool[chat_id] = None
        stop_flag = self.stop_pool[chat_id]
        timeout_flag = self.timeout_pool[chat_id]
        run_error = self.run_error_pool[chat_id]
        _ = self.thread_pool.pop(chat_id)
        _.terminate()
        del _
        self.stop_pool.pop(chat_id)
        self.timeout_pool.pop(chat_id)
        self.run_error_pool.pop(chat_id)
        return stop_flag, timeout_flag, run_error

    def kill_thread(self, chat_id) -> None:
        if chat_id in self.thread_pool and self.thread_pool[chat_id] is not None:
            try:
                self.stop_pool[chat_id] = True
                while self.thread_pool[chat_id].is_alive():
                    self.thread_pool[chat_id].terminate()
            except Exception as e:
                if not self.thread_pool[chat_id].is_alive():
                    self.stop_pool[chat_id] = True
                pass

    def timeout_thread(self, chat_id) -> None:
        if chat_id in self.thread_pool and self.thread_pool[chat_id] is not None:
            try:
                self.timeout_pool[chat_id] = True
                while self.thread_pool[chat_id].is_alive():
                    self.thread_pool[chat_id].terminate()
            except Exception as e:
                if not self.thread_pool[chat_id].is_alive():
                    self.timeout_pool[chat_id] = True
                pass

    def error_thread(self, chat_id, e_msg: str) -> None:
        if chat_id in self.thread_pool and self.thread_pool[chat_id] is not None:
            try:
                self.run_error_pool[chat_id] = e_msg
            except:
                pass
