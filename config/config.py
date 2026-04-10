import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


token=os.getenv("BOT_TOKEN", "")
host=os.getenv("SERVER_HOST", "http://127.0.0.1:8080")
api_path=os.getenv("API_PATH", "/api/v1")
debug_mode=os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "yes")

TEXT = (
    "Сервис временно недоступен. Повторите попытку позже"
    "Если проблема сохраняется, сообщите разработчику @kot_gray"
)
service_unavailable_text = os.getenv("SERVICE_UNAVAILABLE_TEXT", TEXT)

BASE_URL = f"{host}{api_path}"

HELLO_TEXT_PATH = "config/texts/hello.txt"
