"""Зависимости, включаемые при обработке запросов."""
from config import settings
from infrastructure.connector.s3.base.client import S3Client
from infrastructure.connector.sqla.base import async_session
from infrastructure.repository.book import BookRepository
from infrastructure.uow.main import UnitOfWork


def get_uow() -> UnitOfWork:
    """Зависимость UoW."""
    return UnitOfWork(async_session)


def get_book_repository() -> BookRepository:
    """Зависимость репозиторий Книги."""
    return BookRepository(session_maker=async_session)


def get_s3_client() -> S3Client:
    """Зависимость S3Client."""
    return S3Client.from_settings(settings.S3)
