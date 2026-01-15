import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


token=os.getenv("BOT_TOKEN", "")
host=os.getenv("SERVER_HOST", "http://127.0.0.1:8080")
api_path=os.getenv("API_PATH", "/api/v1")
debug_mode=os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "yes")
base_url = f"{host}{api_path}"

text_hello = "config/texts/hello.txt"
