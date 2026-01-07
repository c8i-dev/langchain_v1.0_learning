from utils.models import *
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


# model_deepseek_with_tools = model_deepseek.bind_tools([get_weather])
# resp = model_deepseek_with_tools.invoke("纽约天气怎么样")
# if resp.tool_calls:
#     print(resp.tool_calls)
# else:
#     print(resp.content)

# resp = get_weather.invoke({"city": "纽约"})
# print(resp)

print(get_weather.name)
print(get_weather.description)
print(get_weather.args)
