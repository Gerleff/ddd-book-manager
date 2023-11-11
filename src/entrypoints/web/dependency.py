"""Зависимости, включаемые при обработке запросов."""
from config import settings
from infrastructure.connectors.s3.base.client import S3Client
from infrastructure.connectors.sqla.base import async_session
from infrastructure.uow.main import UnitOfWork


def get_uow() -> UnitOfWork:
    """Зависимость UoW."""
    return UnitOfWork(async_session)


def get_s3_client() -> S3Client:
    """Зависимость S3Client."""
    return S3Client.from_settings(settings.S3)
