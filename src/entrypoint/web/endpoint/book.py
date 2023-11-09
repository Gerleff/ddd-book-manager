"""Эндпоинты для работы с ресурсом Книга."""
import uuid
from typing import Final

from aiohttp import web
from aiohttp.web_request import Request

from entrypoint.web.config import API_V1_PREFIX
from entrypoint.web.schema.book.crud import BookOutputSchema, CreateBookInputSchema, FileInputFieldName
from entrypoint.web.schema.book.list import ListBookOutputSchema, ListBookQueryParams
from entrypoint.web.schema.book.short import BookShortSchema
from entrypoint.web.shared.encoder import jsonable_encoder
from entrypoint.web.shared.exceptions import RequestValidationError, RequestValueError
from entrypoint.web.shared.parse import parse_form_with_file
from service.handlers.book.create import CreateBookHandler
from service.handlers.book.list import ListBookHandler
from service.handlers.book.read import ReadBookHandler

book_router = web.RouteTableDef()
BOOKS_URL_PREFIX: Final = f"{API_V1_PREFIX}/books"


@book_router.post(BOOKS_URL_PREFIX)
async def create_book(request: Request):
    """Эндпоинт для создания книги."""
    raw_input_schema, file_bytes, file_name = await parse_form_with_file(
        request, FileInputFieldName, dict(name=None, author=None, genre=None, date_published=None)
    )
    try:
        dto = CreateBookInputSchema(**raw_input_schema, file_name=file_name)
    except ValueError as exc:
        raise RequestValidationError(str(exc)) from exc

    uow = request.app["uow_fabric"]()
    s3_client = request.app["s3_client_fabric"]()
    handler = CreateBookHandler(uow=uow, s3_client=s3_client)
    book, presigned_url = await handler.execute(dto, file_bytes, file_name)
    result_schema = BookOutputSchema.from_result(book, presigned_url)

    return web.json_response(jsonable_encoder(result_schema), status=201)


@book_router.get(f"{BOOKS_URL_PREFIX}/{{pk}}")
async def read_book(request: Request):
    """Эндпоинт для чтения книги."""
    try:
        pk = uuid.UUID(request.match_info["pk"])
    except ValueError as exc:
        raise RequestValueError("Pk must be uuid.") from exc

    book_repository = request.app["book_repository_fabric"]()
    s3_client = request.app["s3_client_fabric"]()
    handler = ReadBookHandler(s3_client=s3_client, book_repository=book_repository)
    book, presigned_url = await handler.execute(pk)
    result_schema = BookOutputSchema.from_result(book, presigned_url)

    return web.json_response(jsonable_encoder(result_schema))


@book_router.get(BOOKS_URL_PREFIX)
async def list_books(request: Request):
    """Эндпоинт для выдачи списка книг."""
    list_params = ListBookQueryParams.parse_obj(request.query).to_list_params()

    book_repository = request.app["book_repository_fabric"]()
    handler = ListBookHandler(book_repository=book_repository)
    books = await handler.execute(list_params)
    result_schema = ListBookOutputSchema(books=[BookShortSchema.from_orm(book) for book in books])

    return web.json_response(jsonable_encoder(result_schema))
