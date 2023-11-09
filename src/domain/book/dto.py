"""DTO для передачи данных в доменные методы Книги."""
import datetime

from pydantic.v1 import BaseModel

from domain.book.values import BookAuthor, BookGenre, BookName


class CreateBookDTO(BaseModel):
    """DTO для передачи данных при создании Книги."""

    name: BookName
    author: BookAuthor
    genre: BookGenre
    date_published: datetime.date
    file_name: str
