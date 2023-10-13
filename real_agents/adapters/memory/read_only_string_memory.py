from typing import Any, Dict, List

from langchain.schema import BaseMemory


class ReadOnlySharedStringMemory(BaseMemory):
    """A memory wrapper that is read-only and cannot be changed."""

    memory: BaseMemory

    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return self.memory.memory_variables

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Load memory variables from memory."""
        prev_memory_state = self.memory.return_messages
        self.memory.return_messages = False
        memory_string = self.memory.load_memory_variables(inputs)
        self.memory.return_messages = prev_memory_state
        return memory_string

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Nothing should be saved or changed"""
        pass

    def clear(self) -> None:
        """Nothing to clear, got a memory like a vault."""
        pass
