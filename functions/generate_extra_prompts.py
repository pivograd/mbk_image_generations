import json

from aiohttp import ClientSession

from gemini_client import call_gemini_text
from logger import send_log_to_telegram
from prompts import build_extra_prompts_prompt


async def generate_extra_prompts(
    session: ClientSession,
    mode: str,
) -> list[str]:
    """
    1) Собираем мета-промт для Gemini по mode.
    2) Вызываем Gemini (text).
    3) Достаём строку с JSON-массивом из ответа.
    4) Парсим в list[str] и возвращаем.
    """
    meta_prompt = build_extra_prompts_prompt(mode)
    raw = await call_gemini_text(session, meta_prompt)

    try:
        candidates = raw["candidates"]
        first_candidate = candidates[0]
        parts = first_candidate["content"]["parts"]
        text_field = parts[0]["text"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Неожиданная структура ответа Gemini (text): {e}; raw={raw}")

    try:
        parsed = json.loads(text_field)
    except Exception as e:
        raise RuntimeError(f"Не удалось распарсить JSON из текстового поля Gemini: {e}; text={text_field!r}")

    if not isinstance(parsed, list):
        raise RuntimeError(f"Ожидался JSON-массив, получено: {type(parsed)}")

    return parsed
