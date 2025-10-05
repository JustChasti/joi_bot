from typing import Dict, Any
import aiohttp
from loguru import logger
from services.decorators import handle_errors_async_method


class APIClient:
    """Клиент для работы с API сервера"""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    @handle_errors_async_method
    async def send_message(self, user_id: int, text: str) -> Dict[str, Any]:
        """
        Отправляет сообщение на сервер
        
        Args:
            user_id: ID пользователя Telegram
            content: Текст сообщения
            
        Returns:
            Словарь с ответом от сервера
        """
        self.session = aiohttp.ClientSession()

        payload = {
            "user_id": user_id,
            "content": text
        }
        answer = {
            "text": "Джой приболела и не может ответить, но совсем скоро пойдет на поправку",
            "details": None
        }

        try:
            logger.info(f"Отправка запроса на {self.base_url}: {payload}")
            async with self.session.post(self.base_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = {
                        "text": data["message"],
                        "details": None
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Server returned status {response.status}: {error_text}")
                    answer = {
                        "text": "Джой задремала, но совсем скоро она проснется",
                        "details": error_text
                    }
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            answer = {
                "text": "Джой приболела и не может ответить, но совсем скоро пойдет на поправку",
                "details": str(e)
            }
        await self.session.close()
        self.session = None
        return answer
