"""Настройка подключения к PostgreSQL через SQLAlchemy."""
from pydantic.v1 import BaseSettings, PostgresDsn, validator


class PostgresSettings(BaseSettings):
    """Настройки подключения к Postgres."""

    SERVER: str | None = "localhost"
    USER: str = "admin"
    PASSWORD: str = "password"
    DB: str = "db"
    SCHEMA: str = "public"
    PORT: str = "5432"

    POOL_SIZE: int = 30

    SQLALCHEMY_DATABASE_URI: PostgresDsn | str | None
    SYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn | str | None

    class Config(BaseSettings.Config):
        """Конфигурация настроек."""

        env_prefix = "POSTGRES__"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def _assemble_db_connection(cls, value: str | None, values: dict) -> str:
        """Адрес БД в формате PostgresDSN для использования в SQLAlchemy."""
        if isinstance(value, str):
            return value
        path = values["DB"] or ""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["USER"],
            password=values["PASSWORD"],
            host=values["SERVER"],
            port=values["PORT"],
            path=f"/{path}",
        )

    @validator("SYNC_SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def _assemble_sync_db_connection(cls, value: str | None, values: dict) -> str:  # pylint: disable=W0613
        if uri := values.get("SQLALCHEMY_DATABASE_URI"):
            return uri.replace("postgresql+asyncpg", "postgresql")
        raise ValueError()
