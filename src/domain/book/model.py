"""Доменная модель Книга."""
import datetime

from domain.book.dto import CreateBookDTO
from domain.book.values import BookAuthor, BookGenre, BookName
from domain.shared.base import Entity, StandartEntity, modelclass


@modelclass
class Book(StandartEntity):
    """Сущность Книга."""

    name: BookName
    author: BookAuthor
    genre: BookGenre
    date_published: datetime.date

    file_name: str

    @classmethod
    def create(cls, dto: CreateBookDTO) -> "Book":
        """Создать книгу."""
        return cls(
            name=dto.name,
            author=dto.author,
            genre=dto.genre,
            date_published=dto.date_published,
            file_name=dto.file_name,
        )


@modelclass
class BookAuthorDeniedList(Entity):
    """Серый список авторов книг."""

    value: BookAuthor


@modelclass
class BookNameDeniedList(Entity):
    """Серый список названий книг."""

    value: BookName
