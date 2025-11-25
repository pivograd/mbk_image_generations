from typing import Any, Dict

from aiohttp import web

from functions.generate_image_from_url import generate_image_from_url
from logger import send_log_to_telegram
from prompts import UnknownPromptModeError


async def generate_image(request: web.Request) -> web.Response:
    """
    """
    try:
        data: Dict[str, Any] = await request.json()
    except Exception as e:
        await send_log_to_telegram(f'[generate_image]\nОШИБКА Invalid JSON!\n\n{str(e)}', 'ERROR')
        return web.json_response({"error": "Invalid JSON", "details": str(e)}, status=400)
    try:
        image_url = data.get("image_url")
        mode = data.get("mode", "base")
        extra_text = data.get("extra_text")

        if not image_url:
            await send_log_to_telegram(f'[generate_image]\nНет исходного изображения!\ndata: {data}', 'ERROR')
            return web.json_response({"error": "image_url is required"}, status=400)

        session = request.app["http_session"]
        await send_log_to_telegram(f'[generate_image]\nЗапрос на генерацию изображения!\ndata: {data}','INFO')
        result = await generate_image_from_url(session=session,image_url=image_url, mode=mode, extra_text=extra_text)
        await send_log_to_telegram(f'[generate_image]\nОтвет от ДЖЕМИНИ НАНО БАНАНО ЕПТИ!\nresult: {result} ', 'INFO')
    except UnknownPromptModeError as e:
        await send_log_to_telegram(f'[generate_image]\nОШИБКА Unknown mode!\ndata: {data}\n\nОшибка:{str(e)}', 'ERROR')
        return web.json_response({"error": "Unknown mode", "details": str(e)}, status=400)
    except Exception as e:
        await send_log_to_telegram(f'[generate_image]\nОШИБКА при генерации изображения!\n\n{str(e)}', 'ERROR')
        return web.json_response({"error": "Internal server error", "details": str(e)}, status=500)

    return web.json_response({"result": result})
