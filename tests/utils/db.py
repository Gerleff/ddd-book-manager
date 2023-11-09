import logging
import time
from pathlib import Path

import psycopg2
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from infrastructure.connector.sqla.base import metadata

logger = logging.getLogger(__name__)


class DbConnectionError(Exception):
    """Не удалось соединиться."""


def run_alembic_migration(project_folder: Path, db_dsn: str) -> None:
    logger.info("Run alembic migrate...")

    alembic_config = AlembicConfig(file_=str(project_folder / "src/infrastructure/connector/sqla/alembic/alembic.ini"))
    alembic_config.set_main_option("script_location", str(project_folder / "src/infrastructure/connector/sqla/alembic"))
    alembic_config.set_main_option("sqlalchemy.url", db_dsn)
    alembic_config.set_main_option("ignore_settings", "1")
    alembic_config.cmd_opts = type("", (), {})()
    alembic_upgrade(alembic_config, "head")


def check_db_connection(db_dsn: str, number_of_retries: int = 20) -> None:
    delay = 0.001
    for _ in range(number_of_retries):
        try:
            conn = psycopg2.connect(db_dsn)
        except psycopg2.Error:
            time.sleep(delay)
            delay *= 2
        else:
            conn.close()
            break
    else:
        raise DbConnectionError


def truncate_db_table(db_session: sessionmaker) -> None:
    with db_session.begin() as session:
        for table in reversed(metadata.sorted_tables):
            session.execute(table.delete())


def create_schema(db_session: sessionmaker, schema: str) -> None:
    logger.info(f"Creating the schema '{schema}' ...")

    with db_session.begin() as session:
        session.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))


def prepare_database(db_session: sessionmaker, db_dsn: str, app_path: Path, schema: str) -> None:
    create_schema(db_session, schema)
    run_alembic_migration(app_path, db_dsn)
