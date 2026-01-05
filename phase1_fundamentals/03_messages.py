from utils.models import *
sys_prompt = "你是一个幽默的智能助手，擅长用一句话回答用户的问题"

conversations = [
    {"role":"system","content":sys_prompt}
]

# #### 多轮对话
# conversations.append(
#     {"role":"user","content":"今天是1月1日，明天是几月几日？"}
# )

# resp1 = model_deepseek.invoke(conversations)

# conversations.append(
#     {"role":"assistant","content":resp1.content}
# )

# conversations.append(
#     {"role":"user","content":"后天呢"}
# )

# resp2 = model_deepseek.invoke(conversations)

# conversations.append(
#     {"role":"assistant","content":resp2.content}
# )


##### 对话历史优化，避免太长

def keep_recent_messages(messages: list[dict], max_pairs: int) -> list[dict]:
    """保留最近的N轮对话

    Args:
        messages (list[dict]): 消息列表
        max_pairs (int): 保留的对话轮数，一组user和一组assistant是一轮对话
    Return:
        list[dict]:只保留指定对话轮数的的消息列表
    """

    # 分离系统提示词
    sys_message = [m for m in messages if m.get("role")=="system"]
    conversation = [m for m in messages if m.get("role")!="system"]

    recent_conversation = conversation[-(max_pairs)*2:]

    return sys_message+recent_conversation

while True:
    user_input = input("请输入你的问题：").strip()
    if user_input == "quit":
        break
    elif user_input:
        conversations.append({"role":"user","content":user_input})
        optimized_conversation = keep_recent_messages(conversations,max_pairs=3)

        print(f"***********optimized_conversation**********")
        for con in optimized_conversation:
            print(con)

        try:
            resp = model_deepseek.invoke(optimized_conversation)
            print(f"AI:{resp.content}")
        except Exception as e:
            print(f"未知错误：{e}")
        conversations.append({"role":"assistant","content":resp.content})

    print(f"***********conversations**********")
    for con in conversations:
        print(con)


