from aiohttp.test_utils import TestClient

from entrypoints.web.endpoints.book import BOOKS_URL_PREFIX
from infrastructure.connectors.s3.base.client import S3Client
from tests.api.book.test_create import _get_form_data_from


async def test_s3_not_available(book_model, client: TestClient, monkeypatch):
    async def raises_error(*args, **kwargs):
        raise ConnectionError("S3 not available... for test!")

    monkeypatch.setattr(S3Client, "store_object", raises_error)

    data = _get_form_data_from(book_model)
    async with client.post(f"{BOOKS_URL_PREFIX}", data=data) as response:
        result_json = await response.json()
        assert response.status == 503, result_json
    assert result_json["detail"] == "System is not available. Try again later."
