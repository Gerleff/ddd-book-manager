"""Настройки тестов."""

pytest_plugins = (
    "tests.fixtures.db_models.book",
    "tests.fixtures.common",
    "tests.fixtures.database",
    "tests.fixtures.app",
    "tests.fixtures.s3",
)
