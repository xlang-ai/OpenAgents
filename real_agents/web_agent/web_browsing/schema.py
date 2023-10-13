# The schema (action space) for the web browsing task is defined here:
ACTIONS = [
    {
        "name": "click",
        "description": "Clicks on an element",
        "args": [{"name": "elementId", "type": "number"}],
    },
    {
        "name": "setValue",
        "description": "Focuses on and sets the `value` of an input element.",
        "args": [{"name": "elementId", "type": "number"}, {"name": "value", "type": "string"}],
    },
    {"name": "finish", "description": "Indicates the task is finished", "args": []},
    {"name": "fail", "description": "Indicates that you are unable to complete the task", "args": []},
]
