import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


token=os.getenv("BOT_TOKEN", "")
host=os.getenv("SERVER_HOST", "http://127.0.0.1:8080")
api_path=os.getenv("API_PATH", "/api/v1")
url_send_mesage = f"{host}{api_path}/message"

text_hello = "config/texts/hello.txt"
