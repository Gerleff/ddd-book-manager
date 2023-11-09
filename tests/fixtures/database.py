import logging
from typing import Any, Awaitable, Callable

import pytest
from pydantic.v1 import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings
from infrastructure.connector.sqla.base import async_session
from infrastructure.connector.sqla.mapper import map_database_tables_to_domain_models
from infrastructure.uow.main import UnitOfWork
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


@pytest.fixture(scope="session")
async def db_session(db_async_sessionmaker) -> AsyncSession:
    """Синхронная SQLAlchemy сессия."""
    async with db_async_sessionmaker.begin() as session:
        yield session


@pytest.fixture
def truncate_db(db_sync_sessionmaker):
    """Truncate database after each test, to eliminate the effect of tests on each other."""
    yield
    truncate_db_table(db_sync_sessionmaker)


@pytest.fixture
def test_db(truncate_db):
    """Fixture that aggregates all fixtures that manage(create, migrate, clean etc.) test database.

    If you need to test something that interacts with database, just decorate the test like:
    @pytest.mark.usefixtures("test_db")
    def test_something_with_database(): ...
    """
    yield


@pytest.fixture
def uow(db_async_sessionmaker) -> UnitOfWork:
    return UnitOfWork(db_async_sessionmaker)


@pytest.fixture
async def register_in_db(db_async_sessionmaker, truncate_db) -> Callable[..., Awaitable[Any]]:
    async def wrapper(model):
        async with db_async_sessionmaker.begin() as session:
            session.add(model)

        return model

    return wrapper
