"""Описание UoW."""
from infrastructure.repository.book import BookRepository
from infrastructure.repository.denied_list import BookAuthorDeniedListRepository, BookNameDeniedListRepository
from infrastructure.uow.base import RegisterRepository, RepositoryKeeperUnitOfWork


class UnitOfWork(RepositoryKeeperUnitOfWork):
    """Основной UoW."""

    book_repo: BookRepository = RegisterRepository(BookRepository)
    book_author_denied_list_repo: BookAuthorDeniedListRepository = RegisterRepository(BookAuthorDeniedListRepository)
    book_name_denied_list_repo: BookNameDeniedListRepository = RegisterRepository(BookNameDeniedListRepository)
