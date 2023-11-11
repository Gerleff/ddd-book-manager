"""Обработка запроса на выдачу книг."""
from typing import Sequence

from attrs import define

from domain.book.model import Book
from infrastructure.repository.base.list import ListParamsDTO
from infrastructure.uow.main import UnitOfWork


@define(frozen=True)
class ListBookHandler:
    """Обработчик."""

    uow: UnitOfWork

    async def execute(self, list_params: ListParamsDTO) -> Sequence[Book]:
        """Запуск обработки."""
        async with self.uow:
            return await self.uow.book_repo.read_list(list_params)
