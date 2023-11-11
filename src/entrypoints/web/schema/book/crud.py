"""Схемы для сериализации и десериализации книг."""
import datetime
import uuid
from typing import Final

from pydantic.v1 import AnyUrl, BaseModel

from domain.book.dto import CreateBookDTO
from domain.book.model import Book
from domain.book.values import BookAuthor, BookGenre, BookName

CreateBookInputSchema = CreateBookDTO
CreateBookFileInputFieldName: Final[str] = "file"


class BookOutputSchema(BaseModel):
    """Схема для выдачи книги."""

    id: uuid.UUID
    name: BookName
    author: BookAuthor
    genre: BookGenre
    date_published: datetime.date
    presigned_url: AnyUrl | None

    @classmethod
    def from_result(cls, model: Book, presigned_url: str | None) -> "BookOutputSchema":
        """Генерация схемы из результата обработки."""
        return cls.construct(
            id=model.id,
            name=model.name,
            author=model.author,
            genre=model.genre,
            date_published=model.date_published,
            presigned_url=presigned_url,
        )
