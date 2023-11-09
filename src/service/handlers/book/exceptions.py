"""Исключения при обработке команд про Книги."""
from service.exceptions import ModelNotFoundError


class BookNotFoundError(ModelNotFoundError):
    """Книга не была найдена."""

    message = "Book is not found by provided id."
