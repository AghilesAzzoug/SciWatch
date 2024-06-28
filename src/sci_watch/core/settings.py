from typing import Literal

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Settings class, loaded from .env file
    """

    log_level: Literal[
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"
    ] = Field(env="log_level", default="DEBUG")
    gmail_sender: str = Field(env="gmail_sender")
    gmail_token: str = Field(env="gmail_token")
    grammar_path: str = Field(env="grammar_path")
    http_proxy: str = Field(env="http_proxy", default=None)
    https_proxy: str = Field(env="https_proxy", default=None)
    log_file_path: str = Field(env="log_file_path", default=None)

    class Config:
        allow_mutation = False


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

if settings.log_level in ["NOTSET", "DEBUG"]:
    print("Settings config: ", settings.dict())
