import asyncio
from pathlib import Path

from aiohttp import FormData
from aiohttp.test_utils import TestClient

from entrypoints.web.endpoints.book import BOOKS_URL_PREFIX


_URL = f"{BOOKS_URL_PREFIX}/denied_list/populate"


async def test_populate_ok(client: TestClient):
    _path_to_test_file = (Path(__file__).parents[2] / "files/publisher_decline_list.xlsx").resolve()
    data = FormData()
    data.add_field("file", open(_path_to_test_file, "rb"), filename="publisher_decline_list.xlsx")

    async with client.post(_URL, data=data) as response:
        result_json = await response.json()
        assert response.status == 201
    assert result_json["result"] == "OK"


async def test_concurent(client: TestClient):
    forms = []
    for file in (
        "publisher_decline_list.xlsx", "publisher_decline_list_empty.xlsx", "publisher_decline_list_no_authors.xlsx"
    ):  # nit: для утверждения оптимальности добавить огромные файлы
        _path_to_test_file = (Path(__file__).parents[2] / f"files/{file}").resolve()
        data = FormData()
        data.add_field("file", open(_path_to_test_file, "rb"), filename="publisher_decline_list.xlsx")
        forms.append(data)

    async def _request(form):
        async with client.post(_URL, data=form) as response:
            result_json = await response.json()
            assert response.status == 201
        assert result_json["result"] == "OK"

    result = await asyncio.gather(*[_request(form) for form in forms] * 400)
    assert len(result) == 1200
