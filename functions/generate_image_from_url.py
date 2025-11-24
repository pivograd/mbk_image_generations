from typing import Any, Dict, Optional

from aiohttp import ClientSession

from prompts import build_prompt
from gemini_client import fetch_image_as_base64, call_gemini_with_image


async def generate_image_from_url(session: ClientSession, image_url: str, mode: str, extra_text: Optional[str] = None) -> Dict[str, Any]:
    """
    """
    prompt = build_prompt(mode, extra_text)
    image_b64, mime_type = await fetch_image_as_base64(session, image_url)
    result = await call_gemini_with_image(session, image_b64, mime_type, prompt)
    return result
