import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
current_path = os.path.abspath(__file__)
app.config["UPLOAD_FOLDER"] = os.path.dirname(current_path) + "/data"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# Execute code locally or remotely on docker
app.config["CODE_EXECUTION_MODE"] = os.getenv("CODE_EXECUTION_MODE", "local")
CORS(app)
