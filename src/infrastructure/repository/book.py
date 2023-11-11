"""Репозиторий Книги и доп инструкции."""
from sqlalchemy import and_, or_, select

from domain.book.model import Book
from infrastructure.connectors.sqla.table.book import book_table
from infrastructure.connectors.sqla.table.denied_list import (
    book_author_denied_list_table as author_dl_table,
    book_name_denied_list_table as name_dl_table,
)
from infrastructure.repository.base.base import Query
from infrastructure.repository.base.list import SQLFilter, SQLSorting, SupportsListRepository


class BookRepository(SupportsListRepository):
    """Репозиторий Книги."""

    model = Book

    def _modify_query_with_filters(self, query: Query, filters: list["SQLFilter"]) -> Query:
        for sql_filter in filters:
            if sql_filter.field in book_field_column_map:
                query = sql_filter.modify_query(query, book_field_column_map)
            elif sql_filter.field == "downloadable":
                author_subquery = select(author_dl_table).where(author_dl_table.c.value == book_table.c.author).exists()
                name_subquery = select(name_dl_table).where(name_dl_table.c.value == book_table.c.name).exists()
                if sql_filter.value is True:
                    author_subquery = author_subquery.__invert__()
                    name_subquery = name_subquery.__invert__()
                    clause_operator_ = and_
                else:
                    clause_operator_ = or_
                query = query.filter(clause_operator_(author_subquery, name_subquery))
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
