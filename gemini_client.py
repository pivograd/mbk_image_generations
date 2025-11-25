import base64
import json
from typing import Tuple, Dict, Any, Optional

from aiohttp import ClientSession

from config import GEMINI_API_KEY, GEMINI_API_URL_TEXT, GEMINI_API_URL_IMAGE
from logger import send_log_to_telegram


async def fetch_image_as_base64(session: ClientSession, url: str) -> Optional[tuple[str, str]]:
    """
    Скачивает изображение по URL и возвращает (base64, mime_type).
    """
    try:
        async with session.get(url, timeout=60) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(
                    f"Не удалось скачать изображение: статус {resp.status}, тело: {text}"
                )

            content_type = resp.headers.get("Content-Type", "image/jpeg")
            data = await resp.read()

        b64 = base64.b64encode(data).decode("ascii")
        return b64, content_type
    except Exception as e:
        await send_log_to_telegram(f'[fetch_image_as_base64]\nОшибка при скачивании изображения\n\n{e}', 'ERROR')


async def call_gemini_with_image(session: ClientSession, image_b64: str, mime_type: str, prompt: str) -> Dict[str, Any]:
    """
    Вызывает Gemini API с изображением + текстовым промтом.
    Возвращает JSON-ответ от Gemini как dict.
    """
    parts = [
        {
            "inlineData": {
                "data": image_b64,
                "mimeType": mime_type,
            }
        },
        {
            "text": prompt,
        },
    ]

    body: Dict[str, Any] = {
        "contents": [
            {
                "parts": parts
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }

    params = {"key": GEMINI_API_KEY}

    async with session.post(
        GEMINI_API_URL_IMAGE,
        params=params,
        json=body,
        timeout=120,
    ) as resp:
        text = await resp.text()
        if resp.status != 200:
            raise RuntimeError(f"Ошибка от Gemini API: статус {resp.status}, тело: {text}")

        return await resp.json()



async def call_gemini_text(session: ClientSession, prompt: str) -> Dict[str, Any]:
    """
    Вызывает Gemini для текстовой задачи.
    Мы просим модель вернуть JSON в виде строки в первом parts[0].text.
    Возвращаем сырое тело ответа (как dict).
    """
    body: Dict[str, Any] = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    params = {"key": GEMINI_API_KEY}

    async with session.post(
        GEMINI_API_URL_TEXT,
        params=params,
        json=body,
        timeout=120,
    ) as resp:
        text = await resp.text()
        if resp.status != 200:
            raise RuntimeError(
                f"Ошибка от Gemini API (text): статус {resp.status}, тело: {text}"
            )

        return json.loads(text)
