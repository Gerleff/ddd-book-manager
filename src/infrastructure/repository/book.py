"""Репозиторий Книги и доп инструкции."""
from domain.book.model import Book
from infrastructure.connector.sqla.table.book import book_table
from infrastructure.repository.base.base import Query
from infrastructure.repository.base.list import SQLFilter, SQLSorting, SupportsListRepository


class BookRepository(SupportsListRepository):
    """Репозиторий Книги."""

    model = Book

    def _modify_query_with_filters(self, query: Query, filters: list["SQLFilter"]) -> Query:
        for sql_filter in filters:
            query = sql_filter.modify_query(query, book_field_column_map)
        return query

    def _modify_query_with_sorting(self, query: Query, sorting: list["SQLSorting"]) -> Query:
        for sql_sorting in sorting:
            query = sql_sorting.modify_query(query, book_field_column_map)
        return query


book_field_column_map = {
    "name": book_table.c.name,
    "author": book_table.c.author,
    "genre": book_table.c.genre,
    "date_published": book_table.c.date_published,
    "created_at": book_table.c.created_at,
}
