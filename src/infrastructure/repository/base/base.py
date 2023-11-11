"""Базовый репозиторий."""
from abc import ABC
from typing import TypeVar

from sqlalchemy import Delete, Select, Update

from domain.shared.base import Entity
from domain.shared.values import PrimaryKey
from infrastructure.connectors.sqla.base import SQLASessionContext

RepositoryModel = TypeVar("RepositoryModel", bound=Entity)


class BaseRepository(SQLASessionContext, ABC):
    """Базовый репозиторий."""

    model: RepositoryModel

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
