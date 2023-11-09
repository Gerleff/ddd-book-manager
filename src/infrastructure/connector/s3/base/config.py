"""S3 конфигурация."""
from pydantic.v1 import AnyHttpUrl, BaseSettings


class S3Settings(BaseSettings):
    """Настройки BLOB-хранилище (Minio/S3)."""

    URL: AnyHttpUrl | str = "http://localhost:9000"
    BUCKET: str = "test"
    PRESIGNED_URL_EXP: int = 3600
    ACCESS_KEY: str = "minioadmin"  # default for local dev
    SECRET_KEY: str = "minioadmin"  # default for local dev

    class Config(BaseSettings.Config):
        """Конфигурация настроек."""

        env_prefix = "S3__"
