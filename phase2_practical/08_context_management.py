from langchain.agents.middleware import SummarizationMiddleware

from utils.models import (
    model_minimax,
    model_gemini,
    model_deepseek,
    model_openai,
    model_tongyi,
    model_huanyuan,
)
from utils import tools
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import trim_messages, BaseMessage


# agent = create_agent(
#     model=model_deepseek,
#     tools=[tools.get_weather, tools.get_current_time],
#     system_prompt="你是一个有趣的助手",
#     checkpointer=InMemorySaver(),
#     middleware=[
#         SummarizationMiddleware(
#             model=model_deepseek,
#             trigger=("messages", 4),
#             keep=("messages", 2),
#         ),
#     ],
# )
#
# while True:
#     user = input("请输入用户名：").strip().lower()
#     if user == "exit":
#         break
#     if user:
#         if user == "exit":
#             break
#         user_input = input("你的问题：").strip()
#         config = {"configurable": {"thread_id": user}}
#         resp = agent.invoke(
#             {"messages": [{"role": "user", "content": user_input}]},
#             config,
#         )
#         print(resp)
#         print("*******")
#         for state in agent.get_state_history(config):
#             print(state)
#         print("****************************")
#         print(agent.get_state(config))


##### 手动修剪 trim_messages
# messages = [
#     {"role": "system", "content": "你喜欢讲一句话的冷笑话"},
#     {"role": "user", "content": "你好"},
#     {"role": "assistant", "content": "你好！我是你的AI助手，有什么可以帮你的吗？"},
#     {"role": "user", "content": "讲一个关于苹果的笑话"},
#     {"role": "assistant", "content": "有一天，苹果对香蕉说：“你为什么总是弯着腰？”  "},
#     {"role": "user", "content": "讲一个关于香蕉的笑话"},
#     {"role": "assistant", "content": "有一天，香蕉对粒子说：“你为什么总是那么小？” "},
#     {"role": "user", "content": "讲一个关于水果的笑话"},
#     {"role": "assistant", "content": "有一天，水果很大 "},
#     {"role": "user", "content": "讲一个关于汽车的笑话"},
#     {"role": "assistant", "content": "有一天，汽车很大 "},
# ]
#
#
# def trim_messages_num(messages: list[BaseMessage]) -> int:
#     print(len(messages))
#     for m in messages:
#         print(m.content)
#     return len(messages)


#
#
# trimed_conversations = trim_messages(
#     messages,
#     max_tokens=4,
#     token_counter=trim_messages_num,
#     strategy="last",
#     include_system=True,
#     end_on="human",
# )
#
# print(trimed_conversations)


##### 在agent中集成trim_messages

from langchain.agents.middleware import before_model, AgentState
from langgraph.runtime import Runtime
from typing import Any


def trim_messages_num(messages: list[BaseMessage]) -> int:
    print("********trim_messagee*************")
    print(len(messages))
    for m in messages:
        print(m.content)
    return len(messages)


# @before_model
# def trimed_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#     trimed = trim_messages(
#         state["messages"],
#         max_tokens=4,
#         token_counter=trim_messages_num,
#     )
#     return {"messages": trimed}


@before_model
def trimed_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    original_count = len(state["messages"])

    # 简单粗暴：只保留最后 4 条
    trimed = state["messages"][-4:] if len(state["messages"]) > 4 else state["messages"]

    print(f"\n{'=' * 50}")
    print(f"消息裁剪: {original_count} -> {len(trimed)}")
    print("发送给模型的消息:")
    for i, m in enumerate(trimed):
        print(f"  {i + 1}. [{type(m).__name__}] {m.content}")
    print(f"{'=' * 50}\n")

    return {"messages": trimed}


agent = create_agent(
    model=model_deepseek,
    tools=[],
    system_prompt="角色：一个会简洁说话的助手，只会返回一句不超过10个字的话",
    checkpointer=InMemorySaver(),
    middleware=[trimed_messages],
)


while True:
    user_id = input("输入用户名：").strip()
    if user_id == "exit":
        break
    if user_id:
        user_input = input("question:")
        if user_input == "exit":
            break
        if user_input:
            config = {"configurable": {"thread_id": user_id}}
            resp = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config,
            )
            print(resp)
        print("*************history***************")
        for state in agent.get_state_history(config):
            print(state)
        print("***********************************")
