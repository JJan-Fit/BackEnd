from typing import Annotated

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _parse_csv(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    return [item.strip() for item in value.split(",") if item.strip()]


CsvList = Annotated[list[str], NoDecode, BeforeValidator(_parse_csv)]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "JJan Fit Backend"
    app_version: str = "0.1.0"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    cors_origins: CsvList = []

    database_url: str = "mysql+asyncmy://jjanfit:jjanfit@localhost:3306/jjanfit"
    database_echo: bool = False
    database_auto_create: bool = False


settings = Settings()
