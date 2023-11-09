"""Исключения UoW."""
from infrastructure.exceptions import InfrastructureError


class UoWContextViolationError(InfrastructureError):
    """Нарушение эксплуатации контекста UoW."""

    message = "This is allowed only inside of UOW context manager."
