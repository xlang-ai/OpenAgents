APP_TYPES = ["copilot", "plugins", "webot"]
TIME_STEP = 0.035
TIME_OUT_MAP = {"copilot": 90, "plugins": 300, "webot": 600}
STREAM_BLOCK_TYPES = ["image", "echarts"]
STREAM_TOKEN_TYPES = ["tool", "transition", "execution_result", "error", "kaggle_search", "kaggle_connect", "plain"]
EXECUTION_RESULT_MAX_TOKENS_MAP = {"copilot": 1000, "plugins": 2000, "webot": 20000}

HEARTBEAT_INTERVAL = 10

# define error code
UNAUTH = 401
UNFOUND = 404
OVERLOAD = 503
INTERNAL = 500
UNSUPPORTED = 403

# define models which need extra continue flag
NEED_CONTINUE_MODEL = {"claude-v1", "claude-2"}
DEFAULT_USER_ID = "DefaultUser"
