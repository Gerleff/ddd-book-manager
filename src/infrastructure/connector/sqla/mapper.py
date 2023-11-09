# flake8: noqa
"""Маппинг доменных моделей и таблиц базы данных."""
from functools import lru_cache
from typing import Final

from sqlalchemy.orm import registry

from domain.book.model import Book
from infrastructure.connector.sqla.base import metadata
from infrastructure.connector.sqla.table.book import book_table

mapper_registry = registry(metadata=metadata)
SELECT_IN: Final = "selectin"


@lru_cache(maxsize=None)
def map_database_tables_to_domain_models():  # noqa: WPS213
    """Соотносим доменные модели с таблицами в БД."""
    mapper_registry.map_imperatively(Book, book_table)
    mapper_registry.configure()  # Запускаем сразу, чтобы выловить ошибки
