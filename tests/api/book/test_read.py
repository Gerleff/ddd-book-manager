import asyncio
import uuid

from aiohttp.test_utils import TestClient

from domain.book.model import Book
from entrypoints.web.endpoints.book import BOOKS_URL_PREFIX


async def test_read_ok(book_from_db: Book, client: TestClient):
    async with client.get(f"{BOOKS_URL_PREFIX}/{book_from_db.id}") as response:
        result_json = await response.json()
        assert response.status == 200
    assert result_json["id"] == str(book_from_db.id)
    assert result_json["presigned_url"] is not None


async def test_read_unavailable_ok(unavailable_book_from_db: Book, client: TestClient):
    async with client.get(f"{BOOKS_URL_PREFIX}/{unavailable_book_from_db.id}") as response:
        result_json = await response.json()
        assert response.status == 200
    assert result_json["id"] == str(unavailable_book_from_db.id)
    assert result_json["presigned_url"] is None


async def test_read_404(client: TestClient):
    random_uuid = uuid.uuid4()
    async with client.get(f"{BOOKS_URL_PREFIX}/{random_uuid}") as response:
        result_json = await response.json()
        assert response.status == 404
    assert result_json["detail"] == "Book is not found by provided id."


async def test_read_422(client: TestClient):
    async with client.get(f"{BOOKS_URL_PREFIX}/123") as response:
        result_json = await response.json()
        assert response.status == 422
    assert result_json["detail"] == "Pk must be uuid."


async def test_concurent(book_from_db: Book, unavailable_book_from_db: Book, client: TestClient):
    async def _request(model_id):
        async with client.get(f"{BOOKS_URL_PREFIX}/{model_id}") as response:
            assert response.status in (200, 404), await response.json()
        return model_id

    result = await asyncio.gather(
        *[_request(model) for model in (book_from_db.id, unavailable_book_from_db.id, *([uuid.uuid4()] * 100))] * 10
    )
    assert len(result) == 1020
