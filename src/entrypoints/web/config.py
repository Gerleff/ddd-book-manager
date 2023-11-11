"""Конфигурация веб-приложения."""
from typing import Final

from pydantic.v1 import AnyUrl, BaseSettings

API_V1_PREFIX: Final[str] = "/api/v1"


class WebAppSettings(BaseSettings):
    """Настройки веб-приложения."""

    ADDRESS: AnyUrl | str = "http://127.0.0.1:8001"
    BACKEND_CORS_ORIGINS: str = '["http://localhost"]'
    MAX_FILE_SIZE: int = 10 * 2 ** 20  # 10 Mb

    class Config(BaseSettings.Config):
        """Конфигурация настроек."""

        env_prefix = "SERVER__"
