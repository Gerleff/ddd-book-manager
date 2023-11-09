"""Объекты ценности и ограничения Книги."""
from typing import TypeAlias

from pydantic.v1 import constr

BookName: TypeAlias = constr(min_length=1, max_length=255)
BookAuthor: TypeAlias = constr(min_length=1, max_length=255)
BookGenre: TypeAlias = constr(min_length=1, max_length=64)  # nit: Стоит сделать енумом кмк
