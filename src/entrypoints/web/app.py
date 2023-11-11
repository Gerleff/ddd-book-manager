"""Настройки веб-приложения."""
from aiohttp import web

from entrypoints.web.dependency import get_s3_client, get_uow
from entrypoints.web.endpoints.book import book_router
from entrypoints.web.middleware import setup_middlewares
from infrastructure.connectors.sqla.mapper import map_database_tables_to_domain_models


async def on_start_up(app: web.Application) -> None:
    """Что совершить перед запуском приложения."""
    map_database_tables_to_domain_models()
    app["uow_fabric"] = get_uow
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
