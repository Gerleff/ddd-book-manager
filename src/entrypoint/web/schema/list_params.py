"""Отображение параметров отображения списков в схемах."""
from pydantic.v1 import BaseModel, conint

from config import settings
from infrastructure.repository.base.list import ListParamsDTO, SortOperator, SQLFilter, SQLPagination, SQLSorting


class ListSchema(BaseModel):
    """Схема списка."""

    # Пагинация:
    page_num: conint(ge=1) = 1
    page_size: conint(ge=1, le=settings.PROJECT.MAX_PAGE_SIZE) = settings.PROJECT.DEFAULT_PAGE_SIZE

    def to_list_params(self) -> ListParamsDTO:
        """Подготовить к передаче в нижние слои."""
        return ListParamsDTO(
            filters=self.to_sql_filters(),
            sorting=self.to_sql_sorting(),
            pagination=self.to_sql_pagination(),
        )

    def to_sql_filters(self) -> list[SQLFilter] | None:
        """Преобразование в sql-фильтры."""
        return None

    def to_sql_sorting(self) -> list[SQLSorting] | None:
        """Преобразование в sql-сортировку."""
        # Дефолт для проекта:
        return [SQLSorting(field="created_at", operator=SortOperator.DESC)]

    def to_sql_pagination(self) -> SQLPagination:
        """Преобразование в sql-пагинацию."""
        return SQLPagination(limit=self.page_size, offset=(self.page_num - 1) * self.page_size)
