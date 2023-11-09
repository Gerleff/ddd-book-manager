"""Краткие схемы."""
import datetime
import uuid

from pydantic.v1 import BaseModel

from domain.book.values import BookAuthor, BookGenre, BookName


class BookShortSchema(BaseModel, orm_mode=True):
    """Схема для краткого описания книги."""

    id: uuid.UUID
    name: BookName
    author: BookAuthor
    genre: BookGenre
    date_published: datetime.date
