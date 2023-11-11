import asyncio
from pathlib import Path

import pytest
from aiohttp import FormData
from aiohttp.test_utils import TestClient

from domain.book.model import Book
from entrypoints.web.endpoints.book import BOOKS_URL_PREFIX
from entrypoints.web.shared.encoder import jsonable_encoder

_path_to_test_file = (Path(__file__).parents[2] / "files/Test.docx").resolve()


def _get_form_data_from(model: Book, diff_map: dict | None = None, ignore_fields: tuple = ()) -> FormData:
    if diff_map is None:
        diff_map = {}
    data = FormData()
    if "file" not in ignore_fields:
        data.add_field("file", diff_map.get("file", open(_path_to_test_file, "rb")), filename="Test.docx")
    if "name" not in ignore_fields:
        data.add_field("name", diff_map.get("name", model.name))
    if "author" not in ignore_fields:
        data.add_field("author", diff_map.get("author", model.author))
    if "genre" not in ignore_fields:
        data.add_field("genre", diff_map.get("genre", model.genre))
    if "date_published" not in ignore_fields:
        data.add_field("date_published", diff_map.get("date_published", jsonable_encoder(model.date_published)))
    return data


async def test_create_ok(book_model: Book, client: TestClient):
    data = _get_form_data_from(book_model)
    async with client.post(f"{BOOKS_URL_PREFIX}", data=data) as response:
        result_json = await response.json()
        assert response.status == 201, result_json
    assert result_json["id"] is not None
    assert result_json["presigned_url"] is not None


@pytest.mark.parametrize(
    "field, value", (("date_published", "1111-111-1111"), ("genre", "A" * 65), ("name", "U" * 256), ("author", ""))
)
async def test_create_422_invalid(client: TestClient, book_model: Book, field, value):
    data = _get_form_data_from(book_model, {field: value})
    async with client.post(f"{BOOKS_URL_PREFIX}", data=data) as response:
        result_json = await response.json()
        assert response.status == 422
    assert field in result_json["detail"]


@pytest.mark.parametrize("fields", (("date_published", "name"), ("file",)))
async def test_create_422_absent_fields(client: TestClient, book_model: Book, fields: tuple):
    data = _get_form_data_from(book_model, {}, fields)
    async with client.post(f"{BOOKS_URL_PREFIX}", data=data) as response:
        result_json = await response.json()
        assert response.status == 422, result_json
    assert all(field in result_json["detail"] for field in fields), result_json


async def test_concurent(book_model: Book, unavailable_book_model: Book, client: TestClient):
    async def _request(data):
        async with client.post(f"{BOOKS_URL_PREFIX}", data=data) as response:
            assert response.status == 201, await response.json()
        return True

    result = await asyncio.gather(
        *[_request(data) for data in (_get_form_data_from(book_model), _get_form_data_from(unavailable_book_model))]
        * 20
    )
    assert len(result) == 40
