"""Unit Of Work, обеспечивающий транзакционность взаимодействия с репозиториями."""
from abc import ABC
from typing import Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.repository.base.base import BaseRepository
from infrastructure.uow.exceptions import UoWContextViolationError

UoWType = TypeVar("UoWType", bound="SQLAlchemyUnitOfWork")


class SQLAlchemyUnitOfWork(ABC):
    """Базовый unit of work, заточенный под работу с SQLAlchemy."""

    def __init__(self, session_maker: async_sessionmaker):
        """Конструктор."""
        self._session_maker = session_maker
        self._session: AsyncSession | None = None
        self._inside_context_manager = False

    async def __aenter__(self) -> UoWType:
        """Открытие контекста и транзакции."""
        self._session = self._session_maker()
        self._inside_context_manager = True
        return self

    async def __aexit__(self, *args):
        """Закрытие контекста и откат на случай ошибки."""
        self._session.expunge_all()
        await self.rollback()
        await self._session.close()
        self._inside_context_manager = False

    def check_inside_context_manager(self):
        """Проверить контекст UoW."""
        if not self._inside_context_manager:
            raise UoWContextViolationError()

    async def commit(self) -> None:
        """Подтвердить изменения."""
        self.check_inside_context_manager()
        try:
            await self._session.commit()
        except SQLAlchemyError:
            raise

    async def rollback(self) -> None:
        """Откатить изменения."""
        await self._session.rollback()


class RepositoryKeeperUnitOfWork(SQLAlchemyUnitOfWork):
    """Поддерживающий регистрацию репозиториев UoW."""

    def __init__(self, session_maker: async_sessionmaker):
        """Конструктор."""
        super().__init__(session_maker)
        self._repositories: dict[str:BaseRepository] = {}
        self._init_repositories()

    @classmethod
    def get_repositories(cls) -> dict[str : Type[BaseRepository]] | None:
        """Мапиинг доступных репозиториев."""
        repository_protected_attr_name = f"__{cls.__name__}__repository_cls"
        if not (repositories := getattr(cls, repository_protected_attr_name, None)):
            repositories = {}
            setattr(cls, repository_protected_attr_name, repositories)
        return repositories

    def _init_repositories(self) -> None:
        """Инициализировать репозитории."""
        repository_protected_attr_name = f"__{self.__class__.__name__}__repository_cls"
        repositories = getattr(self, repository_protected_attr_name, {})

        for name, repo in repositories.items():
            repo = repo()
            setattr(self, name, repo)
            self._repositories[name] = repo


class RegisterRepository:
    """Дескриптор для регистрации репозиториев."""

    def __init__(self, repo_class: Type[BaseRepository]) -> None:
        """Конструктор."""
        self._repo_class = repo_class
        self.public_name: str = ...
        self.private_name: str = ...

    def __set_name__(self, uow_cls: Type[RepositoryKeeperUnitOfWork], name: str) -> None:
        """Установить имя репозитория и учесть его в UoW."""
        self.public_name = name
        self.private_name = "_" + name
        uow_cls.get_repositories()[name] = self._repo_class

    def __get__(
        self, uow: RepositoryKeeperUnitOfWork, uow_cls: Type[RepositoryKeeperUnitOfWork] = None
    ) -> BaseRepository:
        """Доступ к экземпляру репозитория."""
        repo_instance: BaseRepository = getattr(uow, self.private_name)
        uow.check_inside_context_manager()
        if uow._session is not repo_instance.session:
            repo_instance.session = uow._session
        return repo_instance

    def __set__(self, uow: RepositoryKeeperUnitOfWork, value: BaseRepository) -> None:
        """Зарегистрировать репозиторий как атрибут UoW."""
        setattr(uow, self.private_name, value)
