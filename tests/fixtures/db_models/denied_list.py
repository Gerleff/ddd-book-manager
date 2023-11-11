from pathlib import Path

import pytest

from domain.book.model import BookAuthorDeniedList, BookNameDeniedList
from entrypoints.service.excel_parse.denied_books import parse_names_and_authors

_PUBLISHER_DECLINE_LIST_PATH = (Path(__file__).parents[2] / "files/publisher_decline_list.xlsx").resolve()


@pytest.fixture
async def populate_denied_lists(register_in_db):
    names, authors = parse_names_and_authors(_PUBLISHER_DECLINE_LIST_PATH)
    await register_in_db(  # noqa
        *[BookAuthorDeniedList(value=author) for author in authors], *[BookNameDeniedList(value=name) for name in names]
    )
