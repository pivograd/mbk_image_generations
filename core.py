from aiohttp import web, ClientSession

from api.generate_extra_prompts_handler import generate_extra_prompts_handler
from api.generate_image import generate_image


async def init_http_session(app: web.Application):
    app["http_session"] = ClientSession()


async def close_http_session(app: web.Application):
    session: ClientSession = app["http_session"]
    await session.close()

def setup_routes(app: web.Application) -> None:
    app.router.add_post("/generate_image", generate_image)
    app.router.add_post("/generate_extra_prompts", generate_extra_prompts_handler)

def create_app() -> web.Application:
    app = web.Application()

    app.on_startup.append(init_http_session)
    app.on_cleanup.append(close_http_session)

    setup_routes(app)

    return app
