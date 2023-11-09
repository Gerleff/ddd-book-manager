"""Средства для извлечения данных из запроса."""
from typing import NamedTuple

from aiohttp.web_request import Request

from config import settings
from entrypoint.web.shared.exceptions import RequestValidationError


class _ParseFormWithFileResult(NamedTuple):
    """Результат парсинга."""

    raw_input_schema: dict[str, None | str]
    file_bytes: bytes
    file_name: str


# ToDO указать допустимые разрешения файла и обыграть кейс с необязательностью
async def parse_form_with_file(  # noqa: C901
    request: Request, file_field_name: str, raw_input_schema: dict[str, None | str]
) -> _ParseFormWithFileResult:
    """Вычитать из формы данные и файл."""
    try:
        reader = await request.multipart()
    except (ValueError, AssertionError):
        raise RequestValidationError(f"Field {file_field_name}: File is not provided.")

    file_bytes, file_name = b"", None

    while field := await reader.next():
        field_name = field.name
        if field_name in raw_input_schema:
            raw_input_schema[field_name] = (await field.read(decode=True)).decode("utf-8")
        elif field_name == file_field_name:
            file_name = field.filename
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

    if file_bytes == b"":
        raise RequestValidationError(f"Field {file_field_name}: File is empty.")
    return _ParseFormWithFileResult(raw_input_schema=raw_input_schema, file_bytes=file_bytes, file_name=file_name)
