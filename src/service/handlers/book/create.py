"""Обработка запроса на создание записи о книги."""
from io import IOBase
from typing import NamedTuple

from attrs import define

from domain.book.dto import CreateBookDTO
from domain.book.model import Book
from infrastructure.connector.s3.base.acid import store_in_s3_atomic
from infrastructure.connector.s3.base.client import S3Client
from infrastructure.connector.s3.service import generate_path_to_store_book_file
from infrastructure.uow.main import UnitOfWork


class _Result(NamedTuple):
    """Результат обработки."""

    book: Book
    presigned_url: str


@define(frozen=True)
class CreateBookHandler:
    """Обработчик."""

    uow: UnitOfWork
    s3_client: S3Client

    async def execute(self, dto: CreateBookDTO, file: IOBase | bytes, file_name: str) -> _Result:
        """Запуск обработки."""
        book = Book.create(dto)
        path = generate_path_to_store_book_file(book)
        async with store_in_s3_atomic(self.s3_client, path=path, obj=file) as presigned_url:
            async with self.uow:
                book = await self.uow.book_repo.create(book)
                await self.uow.commit()
        return _Result(book=book, presigned_url=presigned_url)
