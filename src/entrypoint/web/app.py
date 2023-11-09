"""Настройки веб-приложения."""
from aiohttp import web

from entrypoint.web.dependency import get_book_repository, get_s3_client, get_uow
from entrypoint.web.endpoint.book import book_router
from entrypoint.web.middleware import setup_middlewares
from infrastructure.connector.sqla.mapper import map_database_tables_to_domain_models


async def on_start_up(app: web.Application) -> None:
    """Что совершить перед запуском приложения."""
    map_database_tables_to_domain_models()
    app["uow_fabric"] = get_uow
    app["book_repository_fabric"] = get_book_repository
    app["s3_client_fabric"] = get_s3_client
    await get_s3_client().ensure_bucket()


def create_app() -> web.Application:
    """Фабрика для создания приложения."""
    app = web.Application()

    app.router.add_routes(book_router)
    app.on_startup.append(on_start_up)
    setup_middlewares(app)
    return app


web_app = create_app()
