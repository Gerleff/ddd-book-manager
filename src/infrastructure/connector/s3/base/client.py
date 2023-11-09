"""Клиент Minio/S3 хранилища."""
import json
import uuid
from contextlib import asynccontextmanager
from functools import partial
from io import BytesIO, IOBase
from typing import AsyncContextManager, Awaitable, Container

from aioboto3 import Session
from botocore.exceptions import ClientError
from pydantic import AnyHttpUrl

from .config import S3Settings
from .exceptions import BucketNotExistError
from .service import create_bucket_policy, create_expiration_rule


class S3ObjectProtocol(AsyncContextManager):
    """Протокол S3Object.

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/objectsummary/index.html.
    """

    Bucket: Awaitable["S3BucketProtocol"]

    async def get(self, *args, **kwargs) -> dict:
        """Совершить запрос для получения всего S3Object.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/objectsummary/get.html

        Пример получения содержимого:
            s3_response = await s3_object.get()
            content = await s3_response["Body"].read()
        """


class S3BucketProtocol(AsyncContextManager):
    """Протокол S3Bucket.

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html
    """

    objects: Container  # как в DjangoORM

    async def download_fileobj(self, Key: str, Fileobj: IOBase, ExtraArgs=None, Callback=None, Config=None) -> None:
        """Загрузить объект из корзины в IOBase.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/download_fileobj.html
        """

    async def upload_fileobj(self, Fileobj, Key: str, ExtraArgs=None, Callback=None, Config=None) -> None:
        """Загрузить объект в корзину.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/upload_fileobj.html
        """


class S3Client:
    """Клиент BLOB-хранилища (Minio/S3)."""

    def __init__(
        self,
        url: AnyHttpUrl,
        access_key: str,
        secret_key: str,
        default_bucket_name: str,
        default_presigned_url_exp: int,
    ):
        """Конструктор клиента."""
        self.default_bucket_name = default_bucket_name
        self.default_presigned_url_exp = default_presigned_url_exp
        self.session = Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.client_fabric = partial(self.session.client, "s3", endpoint_url=url)
        self.resource_fabric = partial(self.session.resource, "s3", endpoint_url=url)

    @classmethod
    def from_settings(cls, settings: S3Settings) -> "S3Client":
        """Фабрика для инициализации из настроек."""
        return cls(
            url=settings.URL,
            access_key=settings.ACCESS_KEY,
            secret_key=settings.SECRET_KEY,
            default_bucket_name=settings.BUCKET,
            default_presigned_url_exp=settings.PRESIGNED_URL_EXP,
        )

    # Перед началом работы:
    async def ensure_bucket(self, bucket_name: str | None = None) -> None:
        """Гарантия наличия корзины."""
        bucket_name = bucket_name or self.default_bucket_name
        async with self.resource_fabric() as resource:
            bucket = await resource.Bucket(bucket_name)
            if await bucket.creation_date is None:
                await bucket.create()
                async with self.client_fabric() as client:
                    await client.put_bucket_policy(
                        Bucket=bucket_name,
                        Policy=json.dumps(create_bucket_policy(bucket_name)),
                    )

    async def ensure_bucket_lifecycle(
        self, path: str, days: int, is_active: bool = True, bucket_name: str | None = None
    ) -> None:
        """Гарантия наличия политики эксплуатации корзины (необязательно к выполнению)."""
        bucket_name = bucket_name or self.default_bucket_name
        new_rule = create_expiration_rule(path, days, is_active)
        async with self.client_fabric() as client:
            try:
                response = await client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            except ClientError:
                rules = []
            else:
                rules = response["Rules"]
            for rule in rules:
                if rule["Filter"] == new_rule["Filter"]:
                    rule.update(new_rule)
                    break
            else:
                rules.append({"ID": str(uuid.uuid4()), **new_rule})
            await client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={"Rules": rules},
            )

    # CRUD операции
    async def store_object(
        self, path: str, obj: bytes | IOBase, metadata: dict[str, str] | None = None, bucket_name: str | None = None
    ) -> None:
        """Загрузить объект в Minio/S3."""
        if isinstance(obj, bytes):
            obj = BytesIO(obj)
        elif isinstance(obj, IOBase):
            pass
        else:
            raise TypeError(f"Unexpected obj type to store in S3: {type(obj)}")

        async with self._get_bucket(bucket_name) as bucket:
            extra_args = {"ACL": "public-read"}
            if metadata is not None:
                extra_args["Metadata"] = metadata

            await bucket.upload_fileobj(obj, path, ExtraArgs=extra_args)

    async def delete_objects(self, path: str, suppress: bool = True, bucket_name: str | None = None) -> None:
        """Удалить все объекты, соответствующие данному пути, из Minio/S3."""
        async with self._get_bucket(bucket_name) as bucket:
            objects = bucket.objects.filter(Prefix=path)
            try:
                await objects.delete()
            except ClientError:
                if not suppress:
                    raise

    async def get_presigned_url(self, path: str, exp: int | None = None, bucket_name: str | None = None) -> str | None:
        """Выдать временный урл для чтения.

        :param path: Путь хранения
        :param exp: Время хранения (максимум - 7 дней)
        :param bucket_name: Имя корзины
        """
        try:
            async with self.client_fabric() as client:
                return await client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name or self.default_bucket_name, "Key": path},
                    ExpiresIn=exp or self.default_presigned_url_exp,
                )
        except ClientError:
            return None

    @asynccontextmanager
    async def _get_bucket(self, bucket_name: str | None = None) -> AsyncContextManager[S3BucketProtocol]:
        bucket_name = bucket_name or self.default_bucket_name
        async with self.resource_fabric() as resource:
            bucket = await resource.Bucket(bucket_name)
            if await bucket.creation_date is None:
                raise BucketNotExistError()
            yield bucket
