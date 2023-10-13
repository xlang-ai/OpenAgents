USER_PROMPT = """
history_code = \"\"\"{history_code}\"\"\"
human_question = \"\"\"{question}
# DO NOT use function that will pop up a new window (e.g., PIL & Image.show() is NOT preferable, saving the PIL image is better)
# However, feel free to use matplotlib.pyplot.show()\"\"\"
data = \"\"\"{data}\"\"\"
reference_code = \"\"\"{reference_code}\"\"\"

history_dict = {{
    "history code": history_code,
    "human question": human_question,
    "data": data,
    "reference_code": reference_code,
}}
"""

"""
final format:
user_prompt + reference_prompt + history_prompt
"""
