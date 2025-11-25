from typing import Any

from aiohttp import web

from functions.generate_extra_prompts import generate_extra_prompts
from functions.generate_image_from_url import generate_image_from_url
from logger import send_log_to_telegram
from prompts import UnknownPromptModeError


async def generate_extra_prompts_handler(request: web.Request) -> web.Response:
    """
    """
    try:
        data: dict[str, Any] = await request.json()
    except Exception as e:
        await send_log_to_telegram(f'[generate_extra_prompts_handler]\nОШИБКА Invalid JSON!\n\n{str(e)}', 'ERROR')
        return web.json_response({"error": "Invalid JSON", "details": str(e)}, status=400)
    try:
        mode = data.get("mode", "base")
        session = request.app["http_session"]
        await send_log_to_telegram(f'[generate_extra_prompts_handler]\nЗапрос на генерацию промтов!\ndata: {data}', 'INFO')
        variants = await generate_extra_prompts(session=session, mode=mode)
        image_url = data.get("image_url")
        if not image_url:
            await send_log_to_telegram(f'[generate_extra_prompts_handler]\nНет исходного изображения!\ndata: {data}', 'ERROR')
            return web.json_response({"error": "image_url is required"}, status=400)
        result = await generate_image_from_url(session=session, image_url=image_url, mode=mode)
        return web.json_response({"result_image": result, 'result_variants': variants})
    except UnknownPromptModeError as e:
        await send_log_to_telegram(f'[generate_extra_prompts_handler]\nОШИБКА Unknown mode!\n\n{str(e)}', 'ERROR')
        return web.json_response(
            {"error": "Unknown mode", "details": str(e)},
            status=400,
        )
    except Exception as e:
        await send_log_to_telegram(f'[generate_extra_prompts_handler]\nОШИБКА при генерации промтов!\n\n{str(e)}', 'ERROR')
        return web.json_response({"error": "Internal server error", "details": str(e)}, status=500)
