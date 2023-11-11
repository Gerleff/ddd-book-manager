"""Ошибки обработки запросов."""


class RequestValueError(ValueError):
    """Ошибка проверки переданных значений."""


class RequestValidationError(ValueError):
    """Ошибка валидации данных запроса."""
