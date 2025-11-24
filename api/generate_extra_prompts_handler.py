from typing import Any

from aiohttp import web

from functions.generate_extra_prompts import generate_extra_prompts
from prompts import UnknownPromptModeError


async def generate_extra_prompts_handler(request: web.Request) -> web.Response:
    try:
        data: dict[str, Any] = await request.json()
    except Exception as e:
        return web.json_response(
            {"error": "Invalid JSON", "details": str(e)},
            status=400,
        )

    mode = data.get("mode", "base")

    session = request.app["http_session"]

    try:
        variants = await generate_extra_prompts(session=session, mode=mode)
    except UnknownPromptModeError as e:
        return web.json_response(
            {"error": "Unknown mode", "details": str(e)},
            status=400,
        )
    except Exception as e:
        return web.json_response(
            {"error": "Internal server error", "details": str(e)},
            status=500,
        )

    return web.json_response(
        {
            "mode": mode,
            "variants": variants,
        }
    )
