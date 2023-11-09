import datetime
import pytest

from domain.book.model import Book


@pytest.fixture
def book_model() -> Book:
    return Book(name="Book", author="Author", genre="Biopic", date_published=datetime.date(1999, 12, 3), file_name="1")


@pytest.fixture
async def book_from_db(book_model, register_in_db) -> Book:
    return await register_in_db(book_model)


@pytest.fixture
def another_book_model():
    return Book(
        name="AnotherBook",
        author="AnotherAuthor",
        genre="Drama",
        date_published=datetime.date(1999, 10, 8),
        file_name="2",
    )


@pytest.fixture
async def another_book_from_db(another_book_model, register_in_db) -> Book:
    return await register_in_db(another_book_model)
