from langchain import PromptTemplate

template_base = (
    "{input_string}\nPlease provide {num_questions} natural language questions related to the above contents, "
    "but very different from each other. These questions should be diverse, challenging, "
    "and targeted towards different perspectives. "
    "You should ask these questions like you would ask a human, "
    "but strictly follow the style of your role-playing character.\n"
    "Do not explicitly mention the provided contents; "
    "instead use natural language descriptions for them. "
    "The final result should be a numbered list.".strip() + "\n"
)

QUESTION_SUGGESTION_PROMPT_BASE = PromptTemplate(
    input_variables=["input_string", "num_questions"], template=template_base
)

template_user_profile = (
    "{input_string}\n--------------------\n"
    "{user_description}\n"
    "From now on, you should speak in a style that fully conforms to the given role. \n"
    "Please provide {num_questions} natural language questions related to the above database, "
    "but very different from each other. These questions should be diverse, challenging, "
    "and targeted towards different database tables and columns as well as query types. "
    "You should ask these questions like you would ask a human, "
    "but strictly follow the style of your role-playing character.\n"
    "Do not explicitly mention column or table names in the database; "
    "instead use natural language descriptions for them. "
    "The final result should be a numbered list.".strip() + "\n"
)

QUESTION_SUGGESTION_PROMPT_USER_PROFILE = PromptTemplate(
    input_variables=["input_string", "user_description", "num_questions"], template=template_user_profile
)

template_chat_memory = (
    "{input_string}\n--------------------\n"
    "Here is the conversation between Human and AI.\n"
    "{chat_memory}\n"
    "--------------------\n"
    "Please provide {num_questions} natural language questions related to the above contents, "
    "but very different from each other. These questions should be diverse, challenging, "
    "and targeted towards different perspectives.\n"
    "Keep each questions shorter than 15 words.\n"
    "You should ask these questions like you would ask a human, "
    "but strictly follow the style of your role-playing character.\n"
    "Do not explicitly mention the provided contents; "
    "instead use natural language descriptions for them. "
    "The final result should be a numbered list.".strip() + "\n"
)

QUESTION_SUGGESTION_PROMPT_CHAT_MEMORY = PromptTemplate(
    input_variables=["input_string", "chat_memory", "num_questions"], template=template_chat_memory
)
