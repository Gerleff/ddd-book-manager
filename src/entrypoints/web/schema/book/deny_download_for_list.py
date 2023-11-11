"""Схемы для запрета на загрузку файлов книг."""
from typing import Final

from pydantic.v1 import BaseModel

DenyDownloadBookFileInputFieldName: Final[str] = "file"


class DenyDownloadBookResult(BaseModel):
    """Отображаемый результат обработки запроса на запрет на загрузку файлов книг."""

    result: str = "OK"
