"""Схемы для выдачи списка книг."""
import datetime

from pydantic.v1 import BaseModel

from domain.book.values import BookAuthor, BookGenre, BookName
from entrypoints.web.schema.book.short import BookShortSchema
from entrypoints.web.schema.list_params import ListSchema
from infrastructure.repository.base.list import SQLFilter


class ListBookQueryParams(ListSchema):
    """Query-параметры для уточнения запроса на выдачу списка Книг.

    None здесь подходит тк все поля у книг всегда заполнены. Так-то следует использовать что-то вроде NotSet.
    """

    # Фильтры:
    name: BookName | None = None
    author: BookAuthor | None = None
    genre: BookGenre | None = None
    date_published: datetime.date | None = None
    downloadable: bool | None = None

    def to_sql_filters(self) -> list[SQLFilter] | None:
        """Преобразование в sql-фильтры."""
        filters = []
        if self.name is not None:
            filters.append(SQLFilter("name", self.name))
        if self.author is not None:
            filters.append(SQLFilter("author", self.author))
        if self.genre is not None:
            filters.append(SQLFilter("genre", self.genre))
        if self.date_published is not None:
            filters.append(SQLFilter("date_published", self.date_published))
        if self.downloadable is not None:
            filters.append(SQLFilter("downloadable", self.downloadable))
        return filters or None


class ListBookOutputSchema(BaseModel):
    """Схема выдачи списка книг."""

    books: list[BookShortSchema]
