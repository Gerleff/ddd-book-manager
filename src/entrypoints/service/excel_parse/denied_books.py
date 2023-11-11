"""Функционал по извлечению информации из Excel-файлов о запрещенных к скачиванию книгах."""
import io
from pathlib import Path

import openpyxl
from openpyxl.worksheet._read_only import ReadOnlyWorksheet  # noqa

from domain.book.values import BookAuthor, BookName


# nit: Проверить на необходимость оптимизации в асинхронном приложении
# nit: можно еще добавить валидацию состава страниц
def parse_names_and_authors(file: io.BytesIO | Path | str) -> tuple[tuple[BookName, ...], tuple[BookAuthor, ...]]:
    """Извлекаем информации из Excel-файла о запрещенных к скачиванию книгах."""
    workbook = openpyxl.load_workbook(file, read_only=True)
    result = {}
    for expected_sheet_name in ("name", "author"):
        try:
            sheet: ReadOnlyWorksheet = workbook[expected_sheet_name]
        except KeyError:
            result[expected_sheet_name] = ()
            continue
        result[expected_sheet_name] = tuple(
            str(value[0])
            for value in sheet.iter_rows(min_row=2, max_row=None, min_col=2, max_col=2, values_only=True)
            if value[0]
        )
    workbook.close()
    return result["name"], result["author"]
