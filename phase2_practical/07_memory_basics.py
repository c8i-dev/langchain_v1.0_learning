from utils.models import *
from datetime import datetime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool


@tool
def get_current_time() -> str:
    """获取当前时间

    Retuen:
        返回当前时间
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气

    Args:
        city: 指定的城市

    Returns:
        指定城市的天气信息
    """
    weather_data = {
        "北京": "晴天，温度 15°C，空气质量良好",
        "上海": "多云，温度 18°C，有轻微雾霾",
        "深圳": "阴天，温度 22°C，可能有小雨",
        "成都": "小雨，温度 12°C，湿度较高",
    }
    return weather_data.get(city, f"暂未找到{city}的天气数据")


memory = InMemorySaver()

agent = create_agent(
    model=model_openai,
    tools=[get_weather, get_current_time],
    system_prompt="你是一个有用的助手，用一句话回答用户问题",
    checkpointer=memory,
)

# config_1 = {
#     "configurable": {
#         "thread_id": "1",
#     }
# }
#
# config_2 = {
#     "configurable": {
#         "thread_id": "2",
#     }
# }
#
# resp1 = agent.invoke(
#     {"messages": [{"role": "user", "content": "我叫张三"}]},
#     config_1,
# )
# resp2 = agent.invoke(
#     {"messages": [{"role": "user", "content": "我叫什么？"}]},
#     config_1,
# )
#
# resp3 = agent.invoke(
#     {"messages": [{"role": "user", "content": "我叫什么？"}]},
#     config_2,
# )
#
#
# print(resp3)
# state1 = agent.get_state(config_1)
# state2 = agent.get_state(config_2)
#
# print(state1)
# print(state2)

###### 根据用户的数据来进行配置
# thread_id = []
#
# while True:
#     user_name = input("请输入用户名：").strip().lower()
#     if user_name == "exit":
#         break
#     if user_name:
#         thread_id.append(user_name)
#         user_input = input("请输入你的问题：").strip()
#         if user_input == "exit":
#             break
#         try:
#             resp = agent.invoke(
#                 {"messages": [{"role": "user", "content": user_input}]},
#                 config={"configurable": {"thread_id": user_name}},
#             )
#             print(resp["messages"][-1].content)
#         except Exception as e:
#             print(e)

##### 带工具的返回信息
# config_1 = {"configurable": {"thread_id": 1}}
# resp1 = agent.invoke(
#     {"messages": [{"role": "user", "content": "上海天气怎么样？"}]}, config=config_1
# )
# print(resp1)
#
# resp2 = agent.invoke(
#     {"messages": [{"role": "user", "content": "刚才我问的什么？"}]}, config=config_1
# )
# print(resp2)
# resp3 = agent.invoke(
#     {"messages": [{"role": "user", "content": "和成都比怎么样？"}]}, config=config_1
# )
# print(resp3)
# print(f"**" * 10)
#
# state1 = agent.get_state(config_1)
# print(state1)


##### 带工具的历史记录访问
# thread_id = []
#
# while True:
#     user_name = input("请输入用户名：").strip().lower()
#     if user_name == "exit":
#         break
#     if user_name:
#         thread_id.append(user_name)
#         user_input = input("请输入你的问题：").strip()
#         if user_input == "exit":
#             break
#         try:
#             config = {"configurable": {"thread_id": user_name}}
#             resp = agent.invoke(
#                 {"messages": [{"role": "user", "content": user_input}]},
#                 config=config,
#             )
#             print(type(resp))
#             # print(resp["messages"][-1].content)
#             # print(agent.get_state_history(config))
#             # for state in agent.get_state_history(config):
#             #     print(state)
#         except Exception as e:
#             print(e)

##### 函数来调用


def process_task(task_id: int, user_input: str) -> str:
    config = {"configurable": {"thread_id": task_id}}
    agent_task = create_agent(
        model=model_openai,
        tools=[get_weather, get_current_time],
        checkpointer=memory,
    )
    resp = agent_task.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )
    return resp["messages"][-1].content


print(process_task(1, "你好"))
