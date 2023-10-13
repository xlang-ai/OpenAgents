import os
import warnings
import threading

from backend.app import app
from backend.kernel_publisher import start_kernel_publisher
from backend.utils.threading import ThreadManager
from backend.utils.utils import VariableRegister, init_log
from backend.memory import (
    ChatMemoryManager,
    MessageMemoryManager,
    UserMemoryManager,
)

warnings.filterwarnings("ignore", category=UserWarning)

logger = init_log(
    error=os.path.join(".logging", "error.log"),
    runtime=os.path.join(".logging", "runtime.log"),
    serialize=os.path.join(".logging", "serialize.log"),
    trace=os.path.join(".logging", "trace.log"),
)

VARIABLE_REGISTER_BACKEND = os.environ.get("VARIABLE_REGISTER_BACKEND", "local")
MESSAGE_MEMORY_MANAGER_BACKEND = os.environ.get("MESSAGE_MEMORY_MANAGER_BACKEND", "local")
API_KEY_MEMORY_MANAGER_BACKEND = os.environ.get("API_KEY_MEMORY_MANAGER_BACKEND", "local")
JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND = os.environ.get("JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND", "local")

message_pool: MessageMemoryManager = MessageMemoryManager(name="message_pool", backend=MESSAGE_MEMORY_MANAGER_BACKEND)
grounding_source_pool: ChatMemoryManager = ChatMemoryManager()
api_key_pool: UserMemoryManager = UserMemoryManager(name="api_key_pool", backend=API_KEY_MEMORY_MANAGER_BACKEND)
jupyter_kernel_pool: ChatMemoryManager = ChatMemoryManager(
    name="jupyter_kernel_pool", backend=JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND
)
threading_pool: ThreadManager = ThreadManager()

message_id_register = VariableRegister(name="message_id_register", backend=VARIABLE_REGISTER_BACKEND)

# Monitor kernel and kill long running kernels
if app.config["CODE_EXECUTION_MODE"] == "docker":
    threading.Thread(target=start_kernel_publisher, args=(), daemon=True).start()

if __name__ == "__main__":
    import multiprocess

    multiprocess.set_start_method("spawn", True)
    app.run()
