from typing import Any

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class ExecutorStreamingChainHandler(StreamingStdOutCallbackHandler):
    is_end: bool = False
    _all = []

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """"""
        self._all.append(token)
