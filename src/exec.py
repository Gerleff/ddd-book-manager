from aiohttp import web

from config import settings
from entrypoints.web.app import web_app

if __name__ == "__main__":
    web.run_app(web_app, host=settings.SERVER.ADDRESS.host, port=settings.SERVER.ADDRESS.port)
