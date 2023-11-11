"""Общие исключения при обработке команд про Книги."""
from service.exceptions.shared import ModelNotFoundError


class BookNotFoundError(ModelNotFoundError):
    """Книга не была найдена."""

    message = "Book is not found by provided id."
