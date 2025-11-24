import httpx
from config import TELEGRAM_TOKEN


error = '-5031294341'
info = '-4758243206'

TG_MESSAGE_LIMIT = 4096


async def send_log_to_telegram(message: str, log_level: str = "INFO"):

    if len(message) > TG_MESSAGE_LIMIT:
        message = message[:TG_MESSAGE_LIMIT - 150] + "\n... [обрезано]"

    chat_id = error if log_level == "ERROR" else info

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, data=payload)

        if resp.status_code != 200:
            print(f"Ошибка отправки лога: {resp.text} | MSG: {message}")
