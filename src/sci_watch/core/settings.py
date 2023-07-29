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
    gmail_password: str = Field(env="gmail_password")
    grammar_path: str = Field(env="grammar_path")

    class Config:
        allow_mutation = False


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

if settings.log_level in ["NOTSET", "DEBUG"]:
    print("Settings config: ", settings.dict())
