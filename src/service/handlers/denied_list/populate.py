"""Обработка запроса на пополнение "серого списка"."""
from typing import Sequence

from attrs import define

from domain.book.values import BookAuthor, BookName
from infrastructure.uow.main import UnitOfWork


@define(frozen=True)
class PopulateDeniedListHandler:
    """Обработчик."""

    uow: UnitOfWork

    async def execute(self, authors: Sequence[BookAuthor] | None, names: Sequence[BookName] | None) -> None:
        """Запуск обработки."""
        async with self.uow:
            if authors:
                await self.uow.book_author_denied_list_repo.bulk_create(authors)
            if names:
                await self.uow.book_name_denied_list_repo.bulk_create(names)
