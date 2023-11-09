"""Описание UoW."""
from infrastructure.repository.book import BookRepository
from infrastructure.uow.base import RegisterRepository, RepositoryKeeperUnitOfWork


class UnitOfWork(RepositoryKeeperUnitOfWork):
    """Основной UoW."""

    book_repo: BookRepository = RegisterRepository(BookRepository)
