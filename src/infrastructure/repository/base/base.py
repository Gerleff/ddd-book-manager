"""Базовый репозиторий."""
from abc import ABC
from typing import TypeVar

from sqlalchemy import Delete, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.shared.base import Entity
from domain.shared.values import PrimaryKey

RepositoryModel = TypeVar("RepositoryModel", bound=Entity)


class BaseRepository(ABC):
    """Базовый репозиторий."""

    model: RepositoryModel

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
        """Сессия репозитория."""
        return self._session

    @session.setter
    def session(self, new_session: AsyncSession):
        """Назначить сессию репозитория."""
        self._session = new_session

    async def create(self, model: RepositoryModel) -> RepositoryModel:
        """Создать запись с данными модели в хранилище."""
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model

    async def read(self, pk: PrimaryKey) -> RepositoryModel:
        """Вычитать модель из хранилища."""
        return await self._session.get(self.model, pk)


Query = TypeVar("Query", Select, Update, Delete)
