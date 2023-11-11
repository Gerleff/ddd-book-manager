from pathlib import Path

import pytest

from entrypoints.service.excel_parse.denied_books import parse_names_and_authors

_EXPECTED_NAMES = ("Don quixote", "American psycho", "The Great Gatsby", "Dune", "1984", "man in high castle")
_EXPECTED_AUTHORS = ("George Orwell", "Stephen King", "Theodore Dreiser")


@pytest.mark.parametrize(
    "path, expected_result",
    (
        ("files/publisher_decline_list.xlsx", (_EXPECTED_NAMES, _EXPECTED_AUTHORS)),
        ("files/publisher_decline_list_empty.xlsx", ((), ())),
        ("files/publisher_decline_list_no_authors.xlsx", (_EXPECTED_NAMES, ())),
    ),
)
def test_parse_names_and_authors(path, expected_result):
    _path_to_test_file = (Path(__file__).parents[1] / path).resolve()
    result = parse_names_and_authors(_path_to_test_file)
    assert result == expected_result
