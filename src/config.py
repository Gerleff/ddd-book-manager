"""Глобальные настройки проекта."""
from pydantic.v1 import BaseModel, BaseSettings

from entrypoints.web.config import WebAppSettings
from infrastructure.connectors.s3.base.config import S3Settings
from infrastructure.connectors.sqla.config import PostgresSettings


class ProjectSettings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = True
    MAX_PAGE_SIZE: int = 100
    DEFAULT_PAGE_SIZE: int = 25

    class Config(BaseSettings.Config):
        """Конфигурация настроек."""

        env_prefix = "PROJECT__"


class Settings(BaseModel):
    """Настройки."""

    PROJECT: ProjectSettings = ProjectSettings()
    SERVER: WebAppSettings = WebAppSettings()
    POSTGRES: PostgresSettings = PostgresSettings()
    S3: S3Settings = S3Settings()


settings = Settings()
