from utils.models import *
from langchain.agents import create_agent
from langchain_core.tools import tool
from datetime import datetime


@tool
def get_current_time() -> str:
    """获取当前时间

    Return:
        返回当前时间
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculator(operation: str, a: float, b: float) -> str:
    """执行基本的算数运算

    Args:
        operation (str): 运算类型，支持 "add"(加), "subtract"(减), "multiply"(乘), "divide"(除)
        a (float): 第一个数字
        b (float): 第二个数字

    Returns:
        str: 计算结果字符串
    """

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "错误：除数不能为零",
    }

    if operation not in operations:
        return f"不支持{operation}运算符，仅支持'add'(加), 'subtract'(减), 'multiply'(乘), 'divide'(除)四种运算~"

    try:
        result = operations[operation](a, b)
        return f"{a}{operation}{b}={result}"
    except Exception as e:
        return f"计算错误:{e}"


@tool
def web_search(query: str, num_results: int | None = 3) -> str:
    """在网上搜索信息

    Args:
        query (str): 搜索关键词
        num_results (Optional[int]): 返回结果数量，默认3条

    Returns:
        str: 搜索结果字符串
    """

    # 模拟搜索结果
    mock_results = {
        "Python": [
            "Python官方网站 - https://www.python.org",
            "Python教程 - 菜鸟教程",
            "Python最佳实践 - Real Python",
        ],
        "机器学习": [
            "机器学习入门 - Coursera",
            "Scikit-learn文档",
            "机器学习实战 - GitHub",
        ],
        "LangChain": [
            "LangChain官方文档",
            "LangChain GitHub仓库",
            "LangChain教程 - YouTube",
        ],
    }

    results = []
    for key in mock_results:
        if key.lower() in query.lower():
            results = mock_results[key][:num_results]
            break

    if not results:
        return f"未找到关于'{query}'的结果"

    # 格式化搜索结果
    output = f"搜索'{query}'找到 {len(results)} 条结果：\n"
    for i, result in enumerate(results, 1):
        output += f"{i}.{result}\n"

    return output.strip()


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气

    Args:
        city (str): 城市名称，如"北京"、"上海"

    Returns:
        str: 天气信息字符串
    """

    # 模拟天气数据（实际应用中应调用真实API）
    weather_data = {
        "北京": "晴天，温度 15°C，空气质量良好",
        "上海": "多云，温度 18°C，有轻微雾霾",
        "深圳": "阴天，温度 22°C，可能有小雨",
        "成都": "小雨，温度 12°C，湿度较高",
    }

    return weather_data.get(city, f"抱歉，暂时没有{city}的天气数据")


# agent = create_agent(
#     model=model_deepseek,
#     tools=[get_weather, calculator, get_current_time],
#     system_prompt="你是一个有帮助的助手,注意：当用户提出多个请求时，请一次只调用一个工具，等获取结果后再处理下一个。",
# )


# resp = agent.invoke(
#     {"messages": [{"role": "user", "content": "帮我看看北京现在的天气怎么样？"}]}
# )

###### 打印完整细节
# for i, msg in enumerate(resp["messages"], 1):
#     print(f"--- 消息 {i} ({msg.__class__.__name__}) ---")
#     if hasattr(msg, "content"):
#         print(f"内容：{msg.content}")
#     if hasattr(msg, "tool_calls") and msg.tool_calls:
#         print(f"工具调用：{msg.tool_calls}")


###### 使用MemorySaver进行多轮对话
# from langgraph.checkpoint.memory import MemorySaver

# memory = MemorySaver()
# agent = create_agent(
#     model=model_openai,
#     tools=[get_weather, calculator],
#     system_prompt="你是一个有帮助的助手。",
#     checkpointer=memory,
# )


# config = {"configurable": {"thread_id": "1"}}


# resp1 = agent.invoke(
#     {"messages": [{"role": "user", "content": "北京的天气怎么样？"}]},
#     config=config,
# )
# print(resp1)

# resp2 = agent.invoke(
#     {"messages": [{"role": "user", "content": "和上海比呢？"}]},
#     config=config,
# )
# print(resp2)

# resp3 = agent.invoke(
#     {"messages": [{"role": "user", "content": "和成都比呢？"}]},
#     config=config,
# )
# print(resp3)


##### 多步骤调用
# agent = create_agent(
#     model=model_tongyi,
#     tools=[calculator],
#     system_prompt="你是一个有用的助手",
# )

# resp1 = agent.invoke(
#     {"messages": [{"role": "user", "content": "先算 10 + 20，然后乘以 3"}]},
# )

# tools_call_count = sum(
#     len(msg.tool_calls) if hasattr(msg, "tool_calls") and msg.tool_calls else 0
#     for msg in resp1["messages"]
# )

# sum = 0
# for msg in resp1["messages"]:
#     if hasattr(msg, "tool_calls") and msg.tool_calls:
#         tool_count = len(msg.tool_calls)
#     else:
#         tool_count = 0
#     sum += tool_count


# print(tools_call_count)
# print(sum)


##### 流式输出
agent = create_agent(
    model=model_openai,
    tools=[get_weather, get_current_time],
)
for chunk in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "帮我看看北京现在的天气怎么样？顺便再帮我看看现在几点了？",
            }
        ]
    }
):
    print(f"#-----------------\n{chunk}\n# -----------------")
    # if "messages" in chunk:
    #     lastest_msg = chunk["messages"][-1]
    #     print(lastest_msg.content)
