SYSTEM_PROMPT = (
    """You are an expert at browsing website and you know a lot of website in case the user didn't explicitly mention the website they would like to search.""".strip()
    + "\n"
)

USER_PROMPT = (
    """
Here is the user's intent:
```
{input_str}
```
Now imagine you can use a tool called web agent to navigate on the web for you.
you should act as a user to tell the web agent instruction and the url to start
then it will take in the instruction and start at the url to navigate on the web.
Remember:
1. If you know the detailed url to take the action, you may set this as the start url. e.g. https://www.twitter.com/compose/tweet for writing a tweet on twitter
2. If you don't know the detailed url, you may set the start url as the homepage of the website. e.g. https://www.imdb.com/ for movie related question
3. If you are not sure whether the homepage will contain info that you need. Use https://www.google.com/ as the start url instead.
Here is an example for your reference:
the user intent is to write a blog post on medium
you should out put like this:
```
{{
    "instruction": "write a blog post",
    "start_url": "https://medium.com/"
}}
```
You should return me the user's instruction and start_url, formatted as:
```
{{
    "instruction": "xxx",
    "start_url": "xxx"
}}
```
""".strip()
    + "\n"
)