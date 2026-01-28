from typing import Dict, Any
import aiohttp
from loguru import logger
from config.config import debug_mode
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
            if debug_mode:
                logger.info(f"Отправка запроса на {self.base_url}/message: {payload}")
            async with self.session.post(f"{self.base_url}/message", json=payload) as response:
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

    @handle_errors_async_method
    async def get_user_info(self, admin_id: int, user_id: int) -> Dict[str, Any]:
        """Получить информацию о пользователе"""
        self.session = aiohttp.ClientSession()
        payload = {
            "admin_id": admin_id,
            "user_id": user_id
        }

        try:
            if debug_mode:
                logger.info(f"Запрос информации о пользователе {user_id}")
            async with self.session.post(f"{self.base_url}/admin/get-info", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка {response.status}: {error_text}")
                    return {"error": f"Status {response.status}", "details": error_text}
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"error": "Connection error", "details": str(e)}
        finally:
            await self.session.close()
            self.session = None


    @handle_errors_async_method
    async def set_user_options(self, admin_id: int, user_id: int, options: Dict[str, Any]) -> Dict[str, Any]:
        """Изменить настройки пользователя"""
        self.session = aiohttp.ClientSession()
        payload = {
            "admin_id": admin_id,
            "user_id": user_id,
            "options": options
        }

        try:
            if debug_mode:
                logger.info(f"Изменение настроек пользователя {user_id}")
            async with self.session.patch(f"{self.base_url}/admin/set-options", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка {response.status}: {error_text}")
                    return {"error": f"Status {response.status}", "details": error_text}
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"error": "Connection error", "details": str(e)}
        finally:
            await self.session.close()
            self.session = None


    @handle_errors_async_method
    async def get_all_users(self, admin_id: int) -> Dict[str, Any]:
        """Получить список всех пользователей"""
        self.session = aiohttp.ClientSession()
        params = {"admin_id": admin_id}

        try:
            if debug_mode:
                logger.info("Запрос списка всех пользователей")
            async with self.session.get(f"{self.base_url}/admin/users", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка {response.status}: {error_text}")
                    return {"error": f"Status {response.status}", "details": error_text}
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"error": "Connection error", "details": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def check_admin_rights(self, admin_id: int) -> bool:
        """Проверить права администратора"""
        self.session = aiohttp.ClientSession()
        params = {"admin_id": admin_id}

        try:
            if debug_mode:
                logger.info(f"Проверка прав администратора для {admin_id}")
            async with self.session.get(f"{self.base_url}/admin/check_rights", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("is_admin")
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка {response.status}: {error_text}")
                    return False
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return False
        finally:
            await self.session.close()
            self.session = None
