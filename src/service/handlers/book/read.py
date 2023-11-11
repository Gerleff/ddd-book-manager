"""Обработка запроса на чтение записи книги."""
from typing import NamedTuple

from attrs import define

from domain.book.model import Book
from domain.shared.values import PrimaryKey
from infrastructure.connectors.s3.base.client import S3Client
from infrastructure.connectors.s3.service import generate_path_to_store_book_file
from infrastructure.uow.main import UnitOfWork
from service.exceptions.book.shared import BookNotFoundError


class _Result(NamedTuple):
    """Результат обработки."""

    book: Book
    presigned_url: str


@define(frozen=True)
class ReadBookHandler:
    """Обработчик."""

    uow: UnitOfWork
    s3_client: S3Client

    async def execute(self, pk: PrimaryKey) -> _Result:
        """Запуск обработки."""
        async with self.uow:
            if (book := await self.uow.book_repo.read(pk)) is None:
                raise BookNotFoundError()
            presigned_url = await self._get_presigned_url(book)

        return _Result(book=book, presigned_url=presigned_url)

    async def _get_presigned_url(self, book: Book) -> str | None:
        if await self._is_file_downloadable_for(book):
            return None
        path = generate_path_to_store_book_file(book)
        return await self.s3_client.get_presigned_url(path)

    async def _is_file_downloadable_for(self, book: Book) -> bool:
        author_is_in_denied_list = await self.uow.book_author_denied_list_repo.read(book.author)
        return author_is_in_denied_list or await self.uow.book_name_denied_list_repo.read(book.name)
