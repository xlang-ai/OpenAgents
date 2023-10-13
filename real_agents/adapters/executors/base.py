from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from real_agents.adapters.schema import SQLDatabase


class BaseExecutor(ABC):
    @abstractmethod
    def run(self, user_intent: str, grounding_source: Optional[SQLDatabase]) -> Dict[str, Any]:
        """Run the executor."""
