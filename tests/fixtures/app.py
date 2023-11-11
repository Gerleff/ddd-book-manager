import pytest
from aiohttp.test_utils import TestClient

from entrypoints.web.app import create_app
from entrypoints.web.dependency import get_s3_client


@pytest.fixture(scope="session")
async def s3_client(event_loop):
    s3_client = get_s3_client()
    await s3_client.ensure_bucket()
    yield s3_client


@pytest.fixture
async def client(aiohttp_client, event_loop) -> TestClient:
    return await aiohttp_client(create_app())
