import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY не задан в переменных окружения")

GEMINI_MODEL_TEXT = "gemini-2.0-flash-exp"
GEMINI_API_URL_TEXT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_TEXT}:generateContent?key={GEMINI_API_KEY}"

GEMINI_MODEL_IMAGE = "gemini-2.5-flash-image"
GEMINI_API_URL_IMAGE = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_IMAGE}:generateContent?key={GEMINI_API_KEY}"



TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан в переменных окружения")