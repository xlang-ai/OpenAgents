SYSTEM_PROMPT = (
    """You are acting like plugin system that understand user's needs and call APIs precisely for them.""".strip()
    + "\n"
)

USER_PROMPT = (
    """
Here are the endpoints specs:
```
{specs_str}
```
Here is the input string:
```
{input_str}
```
Select the right endpoint called that can process the input string.
You need to wrap the input str into a json object, so that it could be fed into the function you selected. 
During wrapping, you should:
1. modify the value of each key so that it satisfies the requirements in function specs.For example, if the type of the value should be a number, then you should modify it into a number;
2. ignore the information that is not useful or not applicable to the function you selected.
You fill values into some slots in the input_json, and then call the API. If the API returns a valid output, then you succeed. Otherwise, you fail.
Return the function called and the json object in the following format:
```
{{
    "endpoint": "xxx",
    "input_json":{{
        "xxx": "xxx",
        "xxx": "xxx",
        ...
    }}
}}
```
""".strip()
    + "\n"
)

RETRY_PROMPT = (
    """
Here are the function specs:
```
{specs_str}
```
Here is the input string:
```
{input_str}
```
Select the right function called that can process the input string.
You need to wrap the input str into a json object, so that it could be fed into the function you selected. During wrapping, you should:
1. modify the value of each key so that it satisfies the requirements in function specs.For example, if the type of the value should be a number, then you should modify it into a number.
2. ignore the information that is not useful or not applicable to the function you selected.
Return the function called and the json object in the following format:
```
{{
    "endpoint": "xxx",
    "input_json":{{
        "xxx": "xxx",
        "xxx": "xxx",
        ...
    }}
}}
```
You have tried to call function to process the input string but failed. The output do not have enough information to answer the tool input.
Here is the history of your trials, each element in this list means a trial:
```
{trial_history}
```
You should firstly analyze your trial history, find the value of the key "errors" in the output of each trial and check whether there are any errors
Then you may consider changing the input_json or endpoint based on the error information in your trial history, function specs and the input string.
Return the function called and the json object in the following format:
```
{{
    "endpoint": "xxx",
    "input_json":{{
        "xxx": "xxx",
        "xxx": "xxx",
        ...
    }}
}}
```
""".strip()
    + "\n"
)

STOP_PROMPT = (
    """
Here are the function specs:
```
{specs_str}
```
Here is the input string:
```
{input_str}
```
Here is the output that you get from calling the API:
```
{api_output}
```
You need to decide whether the returned_block contains valid information or not. Some returned_block may not have enough information to answer the tool input, for example, the returned_block may be empty, or return a json that says some kind of answer.
Answer only by 'yes' or 'no'
""".strip()
    + "\n"
)
