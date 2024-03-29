"""Миддлвари и обработка ошибок."""
from aiohttp import web

from config import settings
from entrypoints.web.shared.exceptions import RequestValidationError, RequestValueError
from infrastructure.exceptions import InfrastructureError
from service.exceptions.shared import ServiceError, ServiceErrorType

_error_type_status_map = {
    ServiceErrorType.NOT_FOUND: 404,
    ServiceErrorType.HANDLER: 400,
}


def create_error_middleware():  # noqa: C901
    """Создать обработчик ошибок."""

    @web.middleware
    async def error_middleware(request, handler):  # noqa: C901
        try:
            return await handler(request)
        except (RequestValueError, RequestValidationError) as value_error:
            return web.json_response({"detail": str(value_error)}, status=422)
        except ServiceError as service_exc:
            if status := _error_type_status_map.get(service_exc.error_type):
                return web.json_response({"detail": service_exc.message}, status=status)
            raise
        except InfrastructureError as infra_exc:
            request.protocol.logger.exception(f"Infra error! {infra_exc}")
            return web.json_response({"detail": "System is not available. Try again later."}, status=503)

        except Exception as unexpected_error:
            request.protocol.logger.exception("Error handling request")
            return web.json_response({"detail": str(unexpected_error)}, status=500)

    return error_middleware


def setup_middlewares(app: web.Application) -> None:
    """Установить миддлвари в приложение."""
    error_middleware = create_error_middleware()
    if settings.PROJECT.DEBUG:
        import aiohttp_debugtoolbar

        aiohttp_debugtoolbar.setup(app)
    app.middlewares.append(error_middleware)
