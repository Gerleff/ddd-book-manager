import logging
from typing import Any, Awaitable, Callable

import pytest
from pydantic.v1 import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from infrastructure.connectors.sqla.base import async_session
from infrastructure.connectors.sqla.mapper import map_database_tables_to_domain_models
from tests.utils.db import truncate_db_table

logger = logging.getLogger(__name__)
map_database_tables_to_domain_models()


@pytest.fixture(scope="session")
def db_dsn() -> str:
    return PostgresDsn.build(
        scheme="postgresql",
        user=settings.POSTGRES.USER,
        password=settings.POSTGRES.PASSWORD,
        host=settings.POSTGRES.SERVER,
        port=settings.POSTGRES.PORT,
        path=f'/{settings.POSTGRES.DB or ""}',
    )


@pytest.fixture(scope="session")
def db_sync_sessionmaker(db_dsn: str) -> sessionmaker:
    """Фабрика для создания синхронной SQLAlchemy сессии."""
    engine = create_engine(db_dsn)
    yield sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def db_async_sessionmaker() -> async_session:
    """Фабрика для создания асинхронной SQLAlchemy сессии."""
    yield async_session


@pytest.fixture
def truncate_db(db_sync_sessionmaker):
    """Truncate database after each test, to eliminate the effect of tests on each other."""
    yield
    truncate_db_table(db_sync_sessionmaker)


@pytest.fixture
async def register_in_db(db_async_sessionmaker, truncate_db) -> Callable[..., Awaitable[Any]]:
    async def wrapper(*models):
        async with db_async_sessionmaker.begin() as session:
            for model in models:
                session.add(model)

        return model

    return wrapper
