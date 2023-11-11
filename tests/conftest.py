"""Настройки тестов."""

pytest_plugins = (
    "tests.fixtures.db_models.book",
    "tests.fixtures.db_models.denied_list",
    "tests.fixtures.common",
    "tests.fixtures.database",
    "tests.fixtures.app",
)
