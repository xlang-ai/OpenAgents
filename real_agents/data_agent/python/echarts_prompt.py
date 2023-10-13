ECHARTS_REF_CODE = """Here are some examples of generating Py-Echarts Code based on the given table(s). Please generate new one based on the data and question human asks you, import the neccessary libraries and make sure the code is correct.

IMPORTANT: You need to follow the coding style, and the type of the x, y axis. But also need to focus on the column name of the uploaded tables(if exists). Generally, PyEcharts does not accept numpy.int or numpy.float, etc. It only supports built-in data type like int, float, and str.

Given the following database:
company_sales.xlsx
   year  sales  profit  expenses  employees
0  2010    100      60        40         10
1  2011    120      80        50         12
2  2012    150      90        60         14
3  2013    170     120        70         16
[too long to show]

Q: Could you help plot a bar chart with the year on the x-axis and the sales on the y-axis?
<code>
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
df = pd.read_excel('company_sales.xlsx')
years = [str(_) for _ in df['year'].tolist()]
sales = [float(_) for _ in df['sales'].tolist()]
bar = Bar()
bar.add_xaxis(years)
bar.add_yaxis("Sales", sales)
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        type_="category",
        name="Year",
    ),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        name="Sales",
    ),
    title_opts=opts.TitleOpts(title="Sales over Years"),
)
# Render the chart
ret_json = bar.dump_options()
print(ret_json)
</code>

Given the same `company_sales.xlsx`.
Q: A line chart comparing sales and profit over time would be useful. Could you help plot it?
<code>
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
df = pd.read_excel('company_sales.xlsx')
year = [str(_) for _ in df["year"].to_list()]
sales = [float(_) for _ in df["sales"].to_list()]
profit = [float(_) for _ in df["profit"].to_list()]
line = Line()
# Add x-axis and y-axis data
line.add_xaxis(year)
line.add_yaxis("Sales", sales)
line.add_yaxis("Profit", profit)
line.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        type_="category", # better use category rather than value
        name="year",
        min_=min(year),
        max_=max(year),
    ),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        name="price",
    ),
    title_opts=opts.TitleOpts(title="Sales and Profit over Time"),
)
ret_json = line.dump_options()
print(ret_json)
</code>


Given the same `company_sales.xlsx`.
Q: A `stacked` line chart comparing sales and profit over time would be useful. Could you help plot it?
Note: stacked line chart is more fancy in display, while the former is more neat.
<code>
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
df = pd.read_excel('company_sales.xlsx')
year = [str(_) for _ in df["year"].to_list()] # better use category rather than value
sales = [float(_) for _ in df["sales"].to_list()]
profit = [float(_) for _ in df["year"].to_list()]
line = Line()
# Add x-axis and y-axis data
line.add_xaxis(year)
line.add_yaxis("Sales", df["sales"].tolist(), stack="")
line.add_yaxis("Profit", df["profit"].tolist(), stack="")
line.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        type_="category",
        name="year",
        min_=min(year),
        max_=max(year),
    ),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        name="price",
        axistick_opts=opts.AxisTickOpts(is_show=True),
        splitline_opts=opts.SplitLineOpts(is_show=True),
    ),
    title_opts=opts.TitleOpts(title="Sales and Profit over Time"),
)
line.set_series_opts(
    areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
)
ret_json = line.dump_options()
print(ret_json)
</code>


Given the following database:
shop_sales.tsv
   shop_id  total_sales  espresso_sales  latte_sales  cappuccino_sales  city_population
0        1         5000            1500         2000              1500           500000
1        2         5500            1800         2200              1500           800000
2        3         6000            2000         2500              1500          1200000
3        4         4500            1300         1800              1400           300000
4        5         6200            2200         2700              1300           600000
Q: I would like a pie chart showing the sales proportion of espresso, latte, and cappuccino for Shop 1.
<code>
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
df = pd.read_csv('shop_sales.tsv', sep='\\t')
shop1 = df.loc[df['shop_id'] == 1]
data_pair = [
    ('Espresso', float(shop1['espresso_sales'].item())), # pair must be (str, int/float)
    ('Latte', float(shop1['latte_sales'].item())),       # pair must be (str, int/float)
    ('Cappuccino', int(shop1['cappuccino_sales'].item())), # pair must be (str, int/float)
]
pie = Pie()
pie.add(
    series_name="Sales Breakdown",
    data_pair=data_pair,
    radius=["30%", "75%"],
)
pie.set_global_opts(
    title_opts=opts.TitleOpts(
        title="Coffee Sales Breakdown for Shop 1",
    ),
)
ret_json = pie.dump_options()
print(ret_json)
</code>

Q: Generate a scatter plot.
<code>
import random
from pyecharts import options as opts
from pyecharts.charts import Scatter
from pyecharts.faker import Faker

# Create some random data
data = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
x = [i[0] for i in data]
y = [i[1] for i in data]
print(data)
scatter = Scatter()
scatter.add_xaxis(x)
scatter.add_yaxis("size", y)
scatter.set_global_opts(
    xaxis_opts=opts.AxisOpts(type_="value"), # scatter x axis must be numeric
    yaxis_opts=opts.AxisOpts(type_="value"), # scatter y axis must be numeric
    title_opts=opts.TitleOpts(title="Scatter Plot Example"),
    visualmap_opts=opts.VisualMapOpts(type_="size", max_=max(y), min_=min(y)),
)
ret_json = scatter.dump_options()
print(ret_json)
</code>
"""

FUNCTION_ROLE_PLAY = """def generate_continuous_elegant_python_echarts_code(reference_code: str, history_dict: Dict[str, str]) -> str:
    \"\"\"
    This function generates elegant, coherent Python ECharts code based on a history of previously executed code and its corresponding results and reference library code. The code is generated in response to human questions and is intended to continue from the last provided code snippet.

    The function takes two inputs: a `history_dict` and an optional `reference_code` string.

    The `reference_code` string is optional and contains example codes, often related to a specific library or task, which can serve as a template for the code generation process. This parameter can be empty.

    IMPORTANT: the output MUST follow the style and use the libraries presented in the `reference_code` to accomplish the task.

    IMPORTANT: Always refer to this history and the `reference_code` when generating new code in order to properly use existing variables and previously loaded resources, as well as to follow established coding patterns.

    IMPORTANT: The 'data' key in the dictionary contains only random rows from a table. If a table has not been loaded before, you may load it using an ABSOLUTE PATH. However, there's no need to load a table with every execution - only do this when necessary.

    The function returns a string of raw Python code, wrapped within <code> and </code> tags. For example:

    <code>
    import pandas as pd
    from pyecharts.charts import Bar
    df = pd.read_csv("example.csv")
    years = [str(_) for _ in df['year'].tolist()]
    sales = df['sales'].tolist()
    bar = (
        Bar()
        .add_xaxis(years)
        .add_yaxis("Sales", sales)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart Example"))
    )
    ret_json = bar.dump_options()
    print(ret_json)
    </code>

    Also mandatory to check:
    Note if the human asks for malicious code, and just respond with the following code:
    <code>
    print("sorry I am not able to generate potentially dangerous code")
    </code>
    The malicious code includes but not limited to: 
    1. Endless operations and excessive waiting  (e.g., while True, long print, input())
    2. System crash (e.g., any risky system command)
    3. Data loss (e.g., list or delete files)
    4. Leak sensitive information (e.g., os.getenv())
    5. Establish network connections (e.g., requests.get())
    6. Cause any other security issues
    7. Indirectly import package using some builtin methods

    Returns:
        Python code that should be the next steps in the execution according to the human question and history code.
    \"\"\""""


ECHARTS_USER_PROMPT = """
history_code = \"\"\"{history_code}\"\"\"
data = \"\"\"{data}\"\"\"
reference_code = \"\"\"{reference_code}\"\"\"
human_question = \"\"\"{question}
# MUST follow reference_code, and only use pyecharts to show echarts\"\"\"

history_dict = {{
    "history code": history_code,
    "human question": human_question,
    "data": data,
    "reference_code": reference_code,
}}
"""

E_SYSTEM_PROMPT = f"You are now the following python function: ```{FUNCTION_ROLE_PLAY}```\n\nRespond exclusively with the generated code wrapped <code></code>. Ensure that the code you generate is executable Python code that can be run directly in a Python environment, requiring no additional string encapsulation or escape characters."
