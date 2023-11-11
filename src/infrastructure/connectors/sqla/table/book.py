"""Определение таблицы Книги."""
import uuid

from sqlalchemy import UUID, Column, String, Table, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql.asyncpg import AsyncpgDate

from infrastructure.connectors.sqla.base import metadata

book_table = Table(
    "book",
    metadata,
    Column(
        name="id",
        type_=UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    ),
    Column("name", String(255), nullable=False),
    Column("author", String(255), nullable=False),
    Column("genre", String(64), nullable=False),
    Column("date_published", AsyncpgDate(), nullable=False),
    Column("file_name", String(255), nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), index=True, nullable=False, server_default=func.current_timestamp()),
)
