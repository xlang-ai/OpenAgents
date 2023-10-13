# flake8: noqa
from langchain import PromptTemplate

# Text-to-sql prompt
_DEFAULT_TEMPLATE = """Here are chat histories you may refer to, maybe empty.
{chat_history}

Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, remember to wrap the table names in double quotes.
Use the following format:
Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"
Only use the tables listed below.
{table_info}
Question: {question}"""
PROMPT = PromptTemplate(
    input_variables=["chat_history", "question", "table_info", "dialect"],
    template=_DEFAULT_TEMPLATE,
)


# Few-shot text-to-sql prompt
FEW_SHOT_PREFIX = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Use the following format:
Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"
Here are some examples you can follow:"""
EXAMPLE_PROMPT_TEMPLATE = """{table_info}\nQuestion: {question}\nSQLQuery: {query}"""
EXAMPLE_PROMPT = PromptTemplate(
    input_variables=["table_info", "question", "query"],
    template=EXAMPLE_PROMPT_TEMPLATE,
)
FEW_SHOT_SUFFIX = """
User the tables listed below.
{table_info}
Question: {question}"""
FEW_SHOT_INPUT_VARIABLES = ["question", "table_info", "dialect", "top_k"]
