# flake8: noqa
"""Маппинг доменных моделей и таблиц базы данных."""
from functools import lru_cache
from typing import Final

from sqlalchemy.orm import registry

from domain.book.model import Book, BookAuthorDeniedList, BookNameDeniedList
from infrastructure.connectors.sqla.base import metadata
from infrastructure.connectors.sqla.table.book import book_table
from infrastructure.connectors.sqla.table.denied_list import book_author_denied_list_table, book_name_denied_list_table

mapper_registry = registry(metadata=metadata)
SELECT_IN: Final = "selectin"


@lru_cache(maxsize=None)
def map_database_tables_to_domain_models():  # noqa: WPS213
    """Соотносим доменные модели с таблицами в БД."""
    mapper_registry.map_imperatively(Book, book_table)
    mapper_registry.map_imperatively(BookAuthorDeniedList, book_author_denied_list_table)
    mapper_registry.map_imperatively(BookNameDeniedList, book_name_denied_list_table)
    mapper_registry.configure()  # Запускаем сразу, чтобы выловить ошибки
