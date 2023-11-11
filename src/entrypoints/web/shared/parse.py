"""Средства для извлечения данных из запроса."""
from typing import Container, NamedTuple

from aiohttp import BodyPartReader
from aiohttp.web_request import Request

from config import settings
from entrypoints.web.shared.exceptions import RequestValidationError


class _ParseFormWithFileResult(NamedTuple):
    """Результат парсинга."""

    raw_input_schema: dict[str, None | str]
    file_bytes: bytes
    file_name: str


async def parse_form_with_file(  # noqa: C901
    request: Request,
    file_field_name: str,
    raw_input_schema: dict[str, None | str],
    allowed_file_extensions: Container[str] | None = None,
) -> _ParseFormWithFileResult:
    """Вычитать из формы данные и файл."""
    try:
        reader = await request.multipart()
    except (ValueError, AssertionError):
        raise RequestValidationError(f"Field {file_field_name}: File is not provided.")

    file_bytes, file_name = None, None

    while field := await reader.next():
        field_name = field.name
        if field_name in raw_input_schema:
            raw_input_schema[field_name] = (await field.read(decode=True)).decode("utf-8")
        elif field_name == file_field_name:
            file_name, file_bytes = await _process_file(field, file_field_name, allowed_file_extensions)
    if file_bytes is None:
        raise RequestValidationError(f"Field {file_field_name}: File is empty.")
    return _ParseFormWithFileResult(raw_input_schema=raw_input_schema, file_bytes=file_bytes, file_name=file_name)


# nit: обыграть кейс с необязательностью
async def _process_file(  # noqa: C901
    field: BodyPartReader, file_field_name: str, allowed_file_extensions: Container[str] | None
) -> tuple[str, bytes]:
    file_name, file_bytes = field.filename, b""
    if allowed_file_extensions:
        extension = file_name.split(".")[-1]
        if extension not in allowed_file_extensions:
            raise RequestValidationError(
                f"Field {file_field_name}: allowed file extensions: {allowed_file_extensions}."
            )
    size = 0
    while True:
        chunk = await field.read_chunk()
        if not chunk:
            break
        size += len(chunk)
        if size >= settings.SERVER.MAX_FILE_SIZE:
            raise RequestValidationError(
                f"Field {file_field_name}: Upload of file with size more than {settings.SERVER.MAX_FILE_SIZE} "
                "is not allowed."
            )
        file_bytes += chunk
    if size == 0:
        raise RequestValidationError(f"Field {file_field_name}: File is empty.")
    return file_name, file_bytes
