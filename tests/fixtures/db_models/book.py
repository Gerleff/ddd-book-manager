import datetime

import pytest

from domain.book.model import Book


@pytest.fixture
def book_model() -> Book:
    return Book(
        name="Book",
        author="Author",
        genre="Biopic",
        date_published=datetime.date(1999, 12, 3),
        file_name="stub.zip",
    )


@pytest.fixture
async def book_from_db(book_model, register_in_db) -> Book:
    return await register_in_db(book_model)


@pytest.fixture
def unavailable_book_model(populate_denied_lists):
    return Book(
        name="Dune",
        author="Franklin Patrick Herbert",
        genre="Drama",
        date_published=datetime.date(1999, 10, 8),
        file_name="stub_too.txt",
    )


@pytest.fixture
async def unavailable_book_from_db(unavailable_book_model, register_in_db) -> Book:
    return await register_in_db(unavailable_book_model)
