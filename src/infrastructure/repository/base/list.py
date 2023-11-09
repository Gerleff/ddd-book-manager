"""Поддержка выдачи списков."""
from abc import ABC
from enum import Enum
from typing import Any, Sequence

from attrs import define
from sqlalchemy import select

from config import settings
from infrastructure.repository.base.base import BaseRepository, Query, RepositoryModel


class FilterOperator(str, Enum):
    """Операторы фильтров."""

    EQ = "eq"


filter_operator_method_map = {FilterOperator.EQ: "__eq__"}


@define(frozen=True)
class SQLFilter:
    """Фильтр SQL."""

    field: str
    value: Any
    operator: FilterOperator = FilterOperator.EQ

    def modify_query(self, query: Query, field_column_map: dict) -> Query:
        """Модифицировать запрос согласно фильтру."""
        method = filter_operator_method_map[self.operator]
        column = field_column_map[self.field]
        return query.filter(getattr(column, method)(self.value))


class SortOperator(str, Enum):
    """Операторы сортировки."""

    ASC = "asc"
    DESC = "desc"


@define(frozen=True)
class SQLSorting:
    """Сортировка SQL."""

    field: str
    operator: SortOperator

    def modify_query(self, query: Query, field_column_map: dict) -> Query:
        """Модифицировать запрос согласно сортировке."""
        if self.operator == SortOperator.DESC:
            column = field_column_map[self.field].desc()
        else:
            column = field_column_map[self.field]
        return query.order_by(column)


@define(frozen=True)
class SQLPagination:
    """Пагинация SQL."""

    limit: int
    offset: int


@define(frozen=True)
class ListParamsDTO:
    """Объект передачи данных о критериях выдачи списка."""

    filters: list["SQLFilter"] | None = None
    sorting: list["SQLSorting"] | None = None
    pagination: SQLPagination | None = None


class SupportsListRepository(BaseRepository, ABC):
    """Репозиторий с поддержкой выдачи списков."""

    async def read_list(self, list_params: ListParamsDTO) -> Sequence[RepositoryModel]:
        """Вычитать список моделей из хранилища."""
        query = self.__build_list_query(list_params)
        query_result = await self._session.execute(query)
        return query_result.scalars().all()

    @property
    def _base_list_query(self) -> Query:
        return select(self.model)

    def _modify_query_with_filters(self, query: Query, filters: list["SQLFilter"]) -> Query:
        raise NotImplementedError

    def _modify_query_with_sorting(self, query: Query, sorting: list["SQLSorting"]) -> Query:
        raise NotImplementedError

    def _modify_query_with_pagination(self, query: Query, pagination: SQLPagination) -> Query:
        return query.offset(pagination.offset).limit(pagination.limit)

    def __build_list_query(self, list_params: ListParamsDTO) -> Query:
        query = self._base_list_query
        if list_params.filters is not None:
            query = self._modify_query_with_filters(query, list_params.filters)
        if list_params.sorting is not None:
            query = self._modify_query_with_sorting(query, list_params.sorting)
        if list_params.pagination is not None:
            query = self._modify_query_with_pagination(query, list_params.pagination)
        else:
            query = query.limit(settings.PROJECT.MAX_PAGE_SIZE)
        return query
