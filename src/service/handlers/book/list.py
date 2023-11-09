"""Обработка запроса на выдачу книг."""
from typing import Sequence

from attrs import define

from domain.book.model import Book
from infrastructure.repository.base.list import ListParamsDTO
from infrastructure.repository.book import BookRepository


@define(frozen=True)
class ListBookHandler:
    """Обработчик."""

    book_repository: BookRepository

    async def execute(self, list_params: ListParamsDTO) -> Sequence[Book]:
        """Запуск обработки."""
        async with self.book_repository:
            return await self.book_repository.read_list(list_params)
