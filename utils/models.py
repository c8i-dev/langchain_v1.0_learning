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