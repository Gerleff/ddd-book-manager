import asyncio
from typing import Generator

import pytest_asyncio


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop() -> Generator:
    """Позволяет использовать event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
