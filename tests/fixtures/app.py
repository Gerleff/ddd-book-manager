import pytest
from aiohttp.test_utils import TestClient, TestServer

from entrypoint.web.app import create_app
from entrypoint.web.dependency import get_s3_client


@pytest.fixture(scope="session")
async def s3_client(event_loop):
    s3_client = get_s3_client()
    await s3_client.ensure_bucket()
    yield s3_client


@pytest.fixture
async def client(event_loop) -> TestClient:
    server = TestServer(create_app())
    await server.start_server()
    yield TestClient(server)
    await server.close()
