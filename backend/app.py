import os

from flask import Flask
from flask_cors import CORS
from real_agents.execution_policy import configured_code_execution_mode, LOCAL_EXECUTION_WARNING

app = Flask(__name__)
current_path = os.path.abspath(__file__)
app.config["UPLOAD_FOLDER"] = os.path.dirname(current_path) + "/data"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# Fail closed unless the operator explicitly configures Python execution.
app.config["CODE_EXECUTION_MODE"] = configured_code_execution_mode()
if app.config["CODE_EXECUTION_MODE"] == "local":
    app.logger.warning(LOCAL_EXECUTION_WARNING)
elif app.config["CODE_EXECUTION_MODE"] == "docker":
    app.logger.warning(
        "Docker Python execution selected. The legacy interpreter is not a verified "
        "sandbox for untrusted users. See backend/README.md#python-execution-trust-boundary."
    )
CORS(app)
