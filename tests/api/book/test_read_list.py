import uuid

import pytest
from aiohttp.test_utils import TestClient

from domain.book.model import Book
from entrypoint.web.endpoint.book import BOOKS_URL_PREFIX
from entrypoint.web.shared.encoder import jsonable_encoder


async def test_read_list_empty(client: TestClient):
    async with client.get(f"{BOOKS_URL_PREFIX}") as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    assert result_json["books"] == []


async def test_read_list_ok(book_from_db: Book, another_book_from_db: Book, client: TestClient):
    first_book_id_to_be_shown_on_success: uuid.UUID = (
        book_from_db.id if book_from_db.created_at > another_book_from_db.created_at else another_book_from_db.id
    )

    async with client.get(f"{BOOKS_URL_PREFIX}") as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    books = result_json["books"]

    assert len(books) == 2, result_json
    assert books[0]["id"] == str(first_book_id_to_be_shown_on_success)


@pytest.mark.parametrize("field", ("name", "author", "genre", "date_published"))
async def test_read_list_filter_ok(book_from_db: Book, another_book_from_db: Book, client: TestClient, field):
    async with client.get(
        f"{BOOKS_URL_PREFIX}", params={field: jsonable_encoder(getattr(book_from_db, field))}
    ) as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    books = result_json["books"]

    assert len(books) == 1, result_json
    assert books[0]["id"] == str(book_from_db.id)


async def test_read_list_pagination_ok(book_from_db: Book, another_book_from_db: Book, client: TestClient):
    first_book_id_to_be_shown_on_success, next_one = (
        (book_from_db.id, another_book_from_db.id)
        if book_from_db.created_at > another_book_from_db.created_at
        else (another_book_from_db.id, book_from_db.id)
    )
    async with client.get(f"{BOOKS_URL_PREFIX}", params={"page_size": 1}) as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    books = result_json["books"]

    assert len(books) == 1, result_json
    assert books[0]["id"] == str(first_book_id_to_be_shown_on_success)

    async with client.get(f"{BOOKS_URL_PREFIX}", params={"page_num": 2, "page_size": 1}) as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    books = result_json["books"]

    assert len(books) == 1, result_json
    assert books[0]["id"] == str(next_one)

    async with client.get(f"{BOOKS_URL_PREFIX}", params={"page_num": 3, "page_size": 1}) as response:
        result_json = await response.json()
        assert response.status == 200, result_json
    books = result_json["books"]

    assert books == []
