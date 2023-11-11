"""Репозитории серого списка книг."""
from abc import ABC
from typing import Sequence, TypeAlias

from sqlalchemy.dialects.postgresql import insert

from domain.book.model import BookAuthorDeniedList, BookNameDeniedList
from domain.book.values import BookAuthor, BookName
from infrastructure.repository.base.base import BaseRepository

_ValueType: TypeAlias = BookName | BookAuthor


class BookDeniedListRepository(BaseRepository, ABC):
    """Репозиторий серого списка для книг."""

    async def bulk_create(self, values: Sequence[_ValueType]) -> None:
        """Создать множество записей с подавлением конфликтов."""
        insert_many_arg = tuple({"value": value} for value in values)
        query = insert(self.model).values(insert_many_arg).on_conflict_do_nothing()
        await self._session.execute(query)


class BookAuthorDeniedListRepository(BookDeniedListRepository):
    """Репозиторий серого списка для авторов книг."""

    model = BookAuthorDeniedList


class BookNameDeniedListRepository(BookDeniedListRepository):
    """Репозиторий серого списка для названий книг."""

    model = BookNameDeniedList
