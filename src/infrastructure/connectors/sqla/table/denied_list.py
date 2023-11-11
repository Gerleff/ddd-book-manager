"""Определение таблицы Книги."""
from sqlalchemy import Column, String, Table

from infrastructure.connectors.sqla.base import metadata

book_author_denied_list_table = Table(
    "book_author_denied_list",
    metadata,
    Column(name="value", type_=String(255), primary_key=True),
)

book_name_denied_list_table = Table(
    "book_name_denied_list",
    metadata,
    Column(name="value", type_=String(255), primary_key=True),
)
