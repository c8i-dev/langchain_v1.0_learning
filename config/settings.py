import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import SettingsConfigDict,BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # deepseek
    api_key:str = Field(alias="DEEPSEEK_API_KEY")
    base_url:str = Field(alias="DEEPSEEK_BASE_URL")
    model:str = Field(alias="DEEPSEEK_MODEL")
    model_provider:str = Field(alias="DEEPSEEK_PROVIDER")

    # tongyi
    tongyi_api_key:str = Field(alias="ALIYUN_API_KEY")
    tongyi_base_url:str = Field(alias="ALIYUN_BASE_URL")
    tongyi_model:str = Field(alias="ALIYUN_MODEL")
    tongyi_model_provider:str = Field(alias="ALIYUN_PROVIDER")

    # chatgpt
    opneai_api_key:str = Field(alias="GPTAPI_API_KEY")
    opneai_base_url:str = Field(alias="GPTAPI_BASE_URL")
    opneai_model:str = Field(alias="GPTAPI_MODEL")
    opneai_model_provider:str = Field(alias="GPTAPI_PROVIDER")


    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.api_key)
    print(settings.base_url)
    print(settings.model)
