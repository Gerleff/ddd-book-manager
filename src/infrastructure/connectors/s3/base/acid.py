"""Транзакционные вспомогательные функции."""
from contextlib import asynccontextmanager
from io import IOBase

from infrastructure.connectors.s3.base.client import S3Client
from infrastructure.connectors.s3.base.exceptions import S3OperationError


@asynccontextmanager
async def store_in_s3_atomic(
    s3_client: S3Client,
    path: str,
    obj: bytes | IOBase,
    metadata: dict[str, str] | None = None,
    bucket_name: str | None = None,
) -> str:
    """Обеспечиваем атомарность при загрузке файла в S3."""
    try:
        await s3_client.store_object(path, obj, metadata, bucket_name=bucket_name)
        yield await s3_client.get_presigned_url(path, bucket_name=bucket_name)
    except Exception as exc:
        await s3_client.delete_objects(path, bucket_name=bucket_name)
        raise S3OperationError(str(exc)) from exc
