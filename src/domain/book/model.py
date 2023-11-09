"""Доменная модель Книга."""
import datetime

from domain.book.dto import CreateBookDTO
from domain.book.values import BookAuthor, BookGenre, BookName
from domain.shared.base import Entity, modelclass


@modelclass
class Book(Entity):
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
