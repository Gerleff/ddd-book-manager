"""Исключения инфраструктурного слоя."""


class InfrastructureError(Exception):
    message = "Something wrong in infrastructure layer"

    def __init__(self, message: str | None = None):
        if message is None:
            message = self.__class__.message
        super().__init__(message)
