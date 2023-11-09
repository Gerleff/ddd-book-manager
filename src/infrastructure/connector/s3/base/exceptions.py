"""Исключения S3."""
from infrastructure.exceptions import InfrastructureError


class BucketNotExistError(InfrastructureError):
    """Исключение при попытке обратиться в несуществующий s3 bucket."""

    def __init__(self):
        """Конструктор."""
        super().__init__("The bucket you're trying to access was not created.")


class S3OperationError(InfrastructureError):
    """Исключение при попытке совершить операцию в S3."""

    def __init__(self, details: str):
        """Конструктор."""
        super().__init__(f"S3 operation error: {details}.")
