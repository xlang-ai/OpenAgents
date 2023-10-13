import os
import sys
import base64
from pathlib import Path
from typing import Any, Dict, Tuple, Union

import pandas as pd
import tiktoken
from flask import Request
from sqlalchemy import create_engine
from PIL import Image
from loguru import logger

from real_agents.adapters.data_model import (
    DatabaseDataModel,
    DataModel,
    ImageDataModel,
    TableDataModel,
    KaggleDataModel,
)
from real_agents.data_agent import (
    DataSummaryExecutor,
    TableSummaryExecutor,
    ImageSummaryExecutor,
)
from real_agents.adapters.schema import SQLDatabase
from backend.utils.running_time_storage import get_running_time_storage
from backend.app import app
from backend.schemas import DEFAULT_USER_ID

TABLE_EXTENSIONS = {"csv", "xls", "xlsx", "tsv"}
DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx", "txt"}
DATABASE_EXTENSIONS = {"sqlite", "db"}
IMAGE_EXTENSIONS = {"jpg", "png", "jpeg"}
ALLOW_EXTENSIONS = TABLE_EXTENSIONS | DOCUMENT_EXTENSIONS | DATABASE_EXTENSIONS | IMAGE_EXTENSIONS

LOCAL = "local"
REDIS = "redis"


class VariableRegister:
    def __init__(self, name=None, backend=LOCAL) -> None:
        self.backend = backend
        if self.backend == LOCAL:
            self.variables: Dict[int, Any] = {}
            self.counter = 1
        elif self.backend == REDIS:
            assert name is not None
            self.name = name
            self.counter_name = f"{self.name}:counter"
            self.variables_name = f"{self.name}:variables"
            with app.app_context():
                self.redis_client = get_running_time_storage()
            if not self.redis_client.exists(self.counter_name):
                self.redis_client.set(self.counter_name, 0)
            else:
                logger.bind(msg_head="VariableRegister").debug(
                    f"Reuse the {self.counter_name}({self.redis_client.get(self.counter_name)}) and {self.variables_name}."
                )
        else:
            raise ValueError("Unknown backend option: {}".format(self.backend))

    def add_variable(self, variable: Any) -> int:
        if self.backend == LOCAL:
            variable_id = self.counter
            self.variables[variable_id] = variable
            self.counter += 1
            return variable_id
        elif self.backend == REDIS:
            variable_id = self.redis_client.incrby(self.counter_name, 1)
            self.redis_client.hset(self.variables_name, variable_id, variable)
            return variable_id

    def get_variable(self, variable_id: int) -> Any:
        if self.backend == LOCAL:
            return self.variables.get(variable_id, None)
        elif self.backend == REDIS:
            return self.redis_client.hget(self.variables_name, variable_id)

    def get_variables(self) -> Dict[int, Any]:
        if self.backend == LOCAL:
            return self.variables
        elif self.backend == REDIS:
            return self.redis_client.hgetall(self.variables_name)


def get_user_and_chat_id_from_request_json(request_json: Dict) -> Tuple[str, str]:
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    chat_id = request_json["chat_id"]
    return user_id, chat_id


def get_user_and_chat_id_from_request(request: Request) -> Tuple[str, str]:
    user_id = request.form.get("user_id", DEFAULT_USER_ID)
    chat_id = request.form.get("chat_id")
    return user_id, chat_id


def load_grounding_source(file_path: str) -> Any:
    # TODO: Maybe convert to DataModel here
    suffix = Path(file_path).suffix
    if Path(file_path).is_dir():
        # Assume it is a collection of csv files, usually downloaded from kaggle.
        grounding_source = {}
        for file in Path(file_path).iterdir():
            if file.suffix == ".csv":
                grounding_source[file.as_posix()] = pd.read_csv(file, index_col=False)
            else:
                raise ValueError("Only csv files are allowed in the directory")
    elif suffix == ".csv":
        grounding_source = pd.read_csv(file_path, index_col=False)
    elif suffix == ".tsv" or suffix == ".txt":
        grounding_source = pd.read_csv(file_path, sep="\t")
    elif suffix == ".xlsx" or suffix == ".xls":
        grounding_source = pd.read_excel(file_path)
    elif suffix == ".db" or suffix == ".sqlite":
        engine = create_engine(f"sqlite:///{file_path}")
        grounding_source = SQLDatabase(engine)
        return grounding_source
    elif suffix == ".png" or suffix == ".jpg" or suffix == ".jpeg":
        img = Image.open(file_path)
        with open(file_path, "rb") as image2string:
            converted_string = "data:image/png;base64," + base64.b64encode(image2string.read()).decode("utf-8")
        grounding_source = {
            "base64_string": converted_string,
            "format": img.format,
            "size": img.size,
            "mode": img.mode,
        }
    else:
        raise ValueError("File type not allowed to be set as grounding source")
    return grounding_source


def get_data_model_cls(file_path: str) -> DataModel:
    suffix = Path(file_path).suffix
    if Path(file_path).is_dir():
        data_model_cls = KaggleDataModel
    elif suffix == ".csv":
        data_model_cls = TableDataModel
    elif suffix == ".tsv" or suffix == ".txt":
        raise NotImplementedError("Not implemented yet")
    elif suffix == ".xlsx" or suffix == ".xls":
        data_model_cls = TableDataModel
    elif suffix == ".sqlite" or suffix == ".db":
        data_model_cls = DatabaseDataModel
    elif suffix == ".jpeg" or suffix == ".png" or suffix == ".jpg":
        data_model_cls = ImageDataModel
    else:
        raise ValueError("File type not allowed to be set as grounding source")
    return data_model_cls


def get_data_summary_cls(file_path: str) -> DataSummaryExecutor:
    suffix = Path(file_path).suffix
    if suffix == ".csv":
        data_summary_cls = TableSummaryExecutor
    elif suffix == ".tsv" or suffix == ".txt":
        raise NotImplementedError("Not implemented yet")
    elif suffix == ".xlsx" or suffix == ".xls":
        data_summary_cls = TableSummaryExecutor
    elif suffix == ".sqlite" or suffix == ".db":
        data_summary_cls = TableSummaryExecutor
    elif suffix == ".jpeg" or suffix == ".png" or suffix == ".jpg":
        data_summary_cls = ImageSummaryExecutor
    else:
        raise ValueError("File type not allowed to be set as grounding source")
    return data_summary_cls


def allowed_file(filename: Union[str, Path]) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    suffix = filename.suffix[1:]
    if suffix in ALLOW_EXTENSIONS:
        return True
    else:
        return False


def is_table_file(filename: Union[str, Path]) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    suffix = filename.suffix[1:]
    if suffix in TABLE_EXTENSIONS:
        return True
    else:
        return False


def is_document_file(filename: Union[str, Path]) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    suffix = filename.suffix[1:]
    if suffix in DOCUMENT_EXTENSIONS:
        return True
    else:
        return False


def is_sqlite_file(filename: Union[str, Path]) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    suffix = filename.suffix[1:]
    if suffix in DATABASE_EXTENSIONS:
        return True
    else:
        return False


def is_image_file(filename: Union[str, Path]) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    suffix = filename.suffix[1:]
    if suffix in IMAGE_EXTENSIONS:
        return True
    else:
        return False


def remove_nan(file_path: str) -> None:
    """
    We only support csv file in the current version
    By default, we remove columns that contain only nan values
    For columns that have both nan values and non-nan values, we replace nan values with the mean (number type)
    or the mode (other type)
    """
    if file_path.endswith("csv"):
        df = pd.read_csv(file_path)
        columns = list(df.columns)
        nan_columns = []
        for c in columns:
            if all(list(df[c].isnull())):
                nan_columns.append(c)
        df.drop(columns=nan_columns, inplace=True)
        columns = list(df.columns)
        for c in columns:
            try:
                fillin_value = df[c].mean()
            except Exception:
                fillin_value = df[c].mode()
            df[c].fillna(value=fillin_value, inplace=True)
        df.to_csv(file_path)


def is_valid_input(user_intent: str, max_token_limit: int = 2000) -> bool:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = len(enc.encode(user_intent))
    return tokens <= max_token_limit


def error_rendering(error_message: str) -> str:
    """Map (certain) error message to frontend rendering form, otherwise show
    'internal backend  error'. Currently, only handle OpenAI error message.
    """
    if "openai" in error_message:
        if "Timeout" in error_message:
            return "OpenAI timeout error. Please try again."
        elif "RateLimitError" in error_message:
            return "OpenAI rate limit error. Please try again."
        elif "APIConnectionError" in error_message:
            return "OpenAI API connection error. Please try again."
        elif "InvalidRequestError" in error_message:
            return "OpenAI invalid request error. Please try again."
        elif "AuthenticationError" in error_message:
            return "OpenAI authentication error. Please try again."
        elif "ServiceUnavailableError" in error_message:
            return "OpenAI service unavailable error. Please try again."
    else:
        return "Internal backend error. Please try again."


def init_log(**sink_channel):
    """Initialize loguru log information"""

    # Just for sys.stdout log message
    format_stdout = (
        "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <lvl>{level}</lvl> - {extra[user_id]}++{extra[chat_id]}-><y>{extra[api]}</y> "
        "<LC>{extra[msg_head]}</LC>:{message}"
    )

    # Avoid unexpected KeyError
    # Do not unpack key-value pairs, but save all records.
    format_full_extra = (
        "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <lvl>{level}</lvl> - <c><u>{name}</u></c> | {message} - {extra}"
    )

    logger.remove()

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, format=format_stdout, level="TRACE"),
            dict(
                sink=sink_channel.get("error"),
                format=format_full_extra,
                level="ERROR",
                diagnose=False,
                rotation="1 week",
            ),
            dict(
                sink=sink_channel.get("runtime"),
                format=format_full_extra,
                level="DEBUG",
                diagnose=False,
                rotation="20 MB",
                retention="20 days",
            ),
            dict(
                sink=sink_channel.get("serialize"),
                level="DEBUG",
                diagnose=False,
                serialize=True,
            ),
        ],
        extra={"user_id": "", "chat_id": "", "api": "", "msg_head": ""},
    )

    return logger


def create_personal_folder(user_id: str) -> str:
    # mkdir user folder
    from backend.main import app

    user_folder = os.path.join(app.config["UPLOAD_FOLDER"], user_id)
    os.makedirs(user_folder, exist_ok=True)
    # mkdir chat folder under user folder
    return user_folder
