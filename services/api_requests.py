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
            "user_id": str(user_id),
            "content": text
        }
        data = {
            "details": None
        }

        try:
            logger.info(f"Отправка запроса на {self.base_url}: {payload}")
            async with self.session.post(self.base_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка сервера {response.status}: {error_text}")
                    data = {
                        "error": f"Server returned status {response.status}",
                        "details": error_text
                    }
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            data = {
                "error": "Connection error",
                "details": str(e)
            }
        await self.session.close()
        self.session = None
        return data
