"""Обработка запроса на чтение записи книги."""
from typing import NamedTuple

from attrs import define

from domain.book.model import Book
from domain.shared.values import PrimaryKey
from infrastructure.connector.s3.base.client import S3Client
from infrastructure.connector.s3.service import generate_path_to_store_book_file
from infrastructure.repository.book import BookRepository
from service.handlers.book.exceptions import BookNotFoundError


class _Result(NamedTuple):
    """Результат обработки."""

    book: Book
    presigned_url: str


@define(frozen=True)
class ReadBookHandler:
    """Обработчик."""

    book_repository: BookRepository
    s3_client: S3Client

    async def execute(self, pk: PrimaryKey) -> _Result:
        """Запуск обработки."""
        async with self.book_repository:
            if (book := await self.book_repository.read(pk)) is None:
                raise BookNotFoundError()
        path = generate_path_to_store_book_file(book)
        presigned_url = await self.s3_client.get_presigned_url(path)
        return _Result(book=book, presigned_url=presigned_url)
