"""Фундаментальные значения для SQLAlchemy."""
from abc import ABC

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    str(settings.POSTGRES.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    echo=False,
    pool_reset_on_return=None,
    pool_size=settings.POSTGRES.POOL_SIZE,
)
async_session = async_sessionmaker(autocommit=False, bind=engine, expire_on_commit=False)
naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",  # noqa
    "uq": "uq_%(table_name)s__%(column_0_name)s",  # noqa
    "ck": "ck_%(table_name)s__%(constraint_name)s",  # noqa
    "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",  # noqa
    "pk": "pk_%(table_name)s",  # noqa
}
metadata = MetaData(naming_convention=naming_convention, schema=settings.POSTGRES.SCHEMA)  # type: ignore[arg-type]


class SQLASessionContext(ABC):
    """Поддержка контекста сессии SQLAlchemy."""

    def __init__(self, session: AsyncSession | None = None, session_maker: async_sessionmaker | None = None):
        """Конструктор."""
        self._session: AsyncSession | None = session
        self._session_maker = session_maker

    async def __aenter__(self):
        """Вход в контекст для закрытия сессии на случай использования вне UoW."""
        if self._session_maker:
            self._session = self._session_maker()
        return self

    async def __aexit__(self, *args, **kwargs):
        """Выход из контекста для закрытия сессии на случай использования вне UoW."""
        await self._session.close()

    @property
    def session(self):
        """Доступ к сессии."""
        return self._session

    @session.setter
    def session(self, new_session: AsyncSession):
        """Инъекция существующей сессии."""
        self._session = new_session
