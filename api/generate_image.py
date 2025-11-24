from typing import Any, Dict

from aiohttp import web

from functions.generate_image_from_url import generate_image_from_url
from prompts import UnknownPromptModeError


async def generate_image(request: web.Request) -> web.Response:
    try:
        data: Dict[str, Any] = await request.json()
    except Exception as e:
        return web.json_response({"error": "Invalid JSON", "details": str(e)}, status=400)

    image_url = data.get("image_url")
    mode = data.get("mode", "base")
    extra_text = data.get("extra_text")

    if not image_url:
        return web.json_response({"error": "image_url is required"}, status=400)

    session = request.app["http_session"]

    try:
        result = await generate_image_from_url(session=session,image_url=image_url, mode=mode, extra_text=extra_text)
    except UnknownPromptModeError as e:
        return web.json_response(
            {"error": "Unknown mode", "details": str(e)},
            status=400,
        )
    except Exception as e:
        return web.json_response({"error": "Internal server error", "details": str(e)}, status=500)

    return web.json_response({"result": result})
