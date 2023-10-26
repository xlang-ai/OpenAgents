export const DEFAULT_SYSTEM_PROMPT =
  process.env.NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT ||
  "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.";

export const OPENAI_API_HOST =
  process.env.OPENAI_API_HOST || 'https://api.openai.com';

export const BACKEND_ENDPOINT =
  process.env.NEXT_PUBLIC_BACKEND_ENDPOINT ||
  ('http://localhost:8000' as const);
export const API_ENDPOINT = `${BACKEND_ENDPOINT}/api` as const;

export const API_UPLOAD = `${API_ENDPOINT}/upload` as const;
export const API_CHAT = `${API_ENDPOINT}/chat` as const;
export const API_CHAT_XLANG = `${API_ENDPOINT}/chat_xlang` as const;
export const API_CHAT_XLANG_PLUGIN = `${API_ENDPOINT}/chat_xlang_plugin` as const;
export const API_CHAT_XLANG_WEBOT = `${API_ENDPOINT}/chat_xlang_webot` as const;
export const API_CHAT_XLANG_WEBOT_STATUS = `${API_ENDPOINT}/webot/webot_status` as const;
export const API_CHAT_XLANG_WEBOT_RESET_STATUS = `${API_ENDPOINT}/webot/reset_status` as const;
export const API_RECOMMEND = `${API_ENDPOINT}/recommend` as const;
export const API_GET_PATH_TREE = `${API_ENDPOINT}/file_system/get_path_tree` as const;
export const API_MOVE_FILES = `${API_ENDPOINT}/file_system/move` as const;
export const API_CREATE_FILE_FOLDER = `${API_ENDPOINT}/file_system/create_folder` as const;
export const API_UPDATE_FILE = `${API_ENDPOINT}/file_system/update` as const;
export const API_DELETE_FILE = `${API_ENDPOINT}/file_system/delete` as const;
export const API_GET_DATA = `${API_ENDPOINT}/get_file` as const;
export const API_SNOWFLAKE = `${API_ENDPOINT}/snowflake` as const; // added by masood
export const API_SQL_QUERY = `${API_ENDPOINT}/sql_query` as const; // added by masood
export const API_GET_TABLE_DATA = `${API_ENDPOINT}/get_table_data` as const; // added by masood
export const API_SNOWFLAKE_DISCONNECT = `${API_ENDPOINT}/snowflake_disconnect` as const; // added by masood
export const API_SET_GROUNDING_SOURCE =
  `${API_ENDPOINT}/set_grounding_source` as const;
export const API_APPLY_FILE_TO_CONVERSATION = `${API_ENDPOINT}/file_system/apply` as const;
export const API_DOWNLOAD_FILE = `${API_ENDPOINT}/file_system/download` as const;
export const API_GET_EDA_INSIGHTS = `${API_ENDPOINT}/eda_insight` as const;
export const API_GET_DATAFLOW = `${API_ENDPOINT}/data_flow` as const;
export const API_GET_TABLE_PROFILE =
  `${API_ENDPOINT}/get_table_profile` as const;
export const API_GET_TABLE_ALERT = `${API_ENDPOINT}/alert` as const;
export const API_GET_TABLE_CLEANED = `${API_ENDPOINT}/clean` as const;
export const API_GET_DATA_TOOL_LIST = `${API_ENDPOINT}/data_tool_list` as const;
export const API_GET_TOOL_LIST = `${API_ENDPOINT}/tool_list` as const;
export const API_POST_API_KEY = `${API_ENDPOINT}/api_key` as const
export const API_REGISTER_USER = `${API_ENDPOINT}/user/register` as const;
export const API_REGISTER_USER_EMAIL = `${API_ENDPOINT}/user/register/email` as const;
export const API_REGISTER_USER_EMAIL_CONFIRM = `${API_ENDPOINT}/user/register/email/confirm` as const;
export const API_REGISTER_CONVERSATION = `${API_ENDPOINT}/conversations/register_conversation` as const;
export const API_REGISTER_FOLDER = `${API_ENDPOINT}/conversations/register_folder` as const;
export const API_UPDATE_CONVERSATION = `${API_ENDPOINT}/conversations/update_conversation` as const;
export const API_UPDATE_FOLDER = `${API_ENDPOINT}/conversations/update_folder` as const;
export const API_CONVERSATION_LIST = `${API_ENDPOINT}/conversations/get_conversation_list` as const;
export const API_CLEAR_CONVERSATIONS = `${API_ENDPOINT}/conversations/clear` as const;
export const API_IMPORT_CONVERSATIONS = `${API_ENDPOINT}/conversations/import` as const;
export const API_DELETE_CONVERSATION = `${API_ENDPOINT}/conversations/delete_conversation` as const;
export const API_DELETE_FOLDER = `${API_ENDPOINT}/conversations/delete_folder` as const;
export const API_GET_CONVERSATION = `${API_ENDPOINT}/conversation` as const;
export const API_GET_FOLDER_LIST = `${API_ENDPOINT}/conversations/get_folder_list` as const;
export const API_STOP_CONVERSATION = `${API_ENDPOINT}/conversations/stop_conversation` as const;
export const API_KAGGLE_DOWNLOAD_DATASET = `${API_ENDPOINT}/kaggle/download_dataset` as const;
export const API_SET_EXAMPLES = `${API_ENDPOINT}/set_default_examples` as const;
export const API_GET_LLM_LIST = `${API_ENDPOINT}/llm_list` as const;
export const API_GET_QUOTA = `${API_ENDPOINT}/user_quota` as const;

export const DEFAULT_TEMPERATURE = parseFloat(
  process.env.NEXT_PUBLIC_DEFAULT_TEMPERATURE || '0.7',
);

export const OPENAI_API_TYPE = process.env.OPENAI_API_TYPE || 'openai';

export const OPENAI_API_VERSION =
  process.env.OPENAI_API_VERSION || '2023-03-15-preview';

export const OPENAI_ORGANIZATION = process.env.OPENAI_ORGANIZATION || '';

export const AZURE_DEPLOYMENT_ID = process.env.AZURE_DEPLOYMENT_ID || '';
