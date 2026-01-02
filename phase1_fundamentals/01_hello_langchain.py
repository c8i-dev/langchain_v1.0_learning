from config.settings import settings
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage


deepseek_model = init_chat_model(
    model = settings.model,
    model_provider = settings.model_provider,
    api_key = settings.api_key,
    base_url = settings.base_url,
    temperature = 1.0,
    max_tokens = 100,
)

tongyi_model = init_chat_model(
    model = settings.tongyi_model,
    model_provider = settings.tongyi_model_provider,
    api_key = settings.tongyi_api_key,
    base_url = settings.tongyi_base_url,
    temperature = 1.0,
    max_tokens = 1000,
)

openai_model = init_chat_model(
    model = settings.opneai_model,
    model_provider = settings.opneai_model_provider,
    api_key = settings.opneai_api_key,
    base_url = settings.opneai_base_url,
    temperature = 1.0,
    max_tokens = 50,
)

messages = [
    SystemMessage(content="你是一个有趣的诗人"),
    HumanMessage(content="写一首关于秋天的诗")
]


# response = openai_model.invoke(messages)
# print("**********ai回复********")
# print(response.content)

# messages.append({"role":"assistant","content":response.content})
# print("********打印消息列表*********")
# print(messages)

# messages.append(HumanMessage(content="再通俗一点呢?"))
# response1 = openai_model.invoke(messages)
# print("**********ai回复********")
# print(response1.content)

# messages.append({"role":"assistant","content":response1.content})
# print("********打印消息列表*********")
# print(messages)
try:
    resp = deepseek_model.stream(messages)
    for chunk in resp:
        print(chunk.content,end="",flush=True)
except Exception as e:
    print(f"未知错误:{e}")