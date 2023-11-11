"""Общие исключения обработки команд."""
from enum import Enum, auto


class ServiceErrorType(Enum):
    """Типы ошибок при обработке."""

    NOT_FOUND = auto()
    HANDLER = auto()


class ServiceError(Exception):
    """Базовая сервисная ошибка."""

    message = "Service error."
    error_type = ServiceErrorType.HANDLER


class ModelNotFoundError(ServiceError):
    """Ошибка отсутсвия модели."""

    message = "Model not found error."
    error_type = ServiceErrorType.NOT_FOUND
