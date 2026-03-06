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
            text: Текст сообщения

        Returns:
            Словарь с ответом от сервера {"success": bool, "message": str}
        """
        self.session = aiohttp.ClientSession()
        payload = {
            "user_id": user_id,
            "content": text
        }

        try:
            if debug_mode:
                logger.info(f"Отправка запроса на {self.base_url}/message: {payload}")
            async with self.session.post(f"{self.base_url}/message", json=payload) as response:
                data = await response.json()
                if response.status != 200:
                    logger.error(f"Server returned status {response.status}: {data}")
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {
                "success": False,
                "message": "Джой приболела и не может ответить, но совсем скоро пойдет на поправку"
            }
        finally:
            await self.session.close()
            self.session = None

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

    @handle_errors_async_method
    async def get_subscription_status(self, telegram_id: int) -> Dict[str, Any]:
        """Получить статус подписки пользователя"""
        self.session = aiohttp.ClientSession()
        params = {"telegram_id": telegram_id}
        try:
            async with self.session.get(f"{self.base_url}/subscription/status", params=params) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def get_pricing_stars(self) -> Dict[str, Any]:
        """Получить цены в звёздах"""
        self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(f"{self.base_url}/subscription/pricing-stars") as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def activate_subscription(
        self,
        telegram_id: int,
        plan: str,
        telegram_payment_id: str,
        amount: int,
        provider: str
    ) -> Dict[str, Any]:
        """Активировать подписку после оплаты"""
        self.session = aiohttp.ClientSession()
        payload = {
            "telegram_id": telegram_id,
            "plan": plan,
            "telegram_payment_id": telegram_payment_id,
            "amount": amount,
            "provider": provider
        }
        try:
            async with self.session.post(f"{self.base_url}/subscription/activate", json=payload) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def delete_user(self, admin_id: int, user_id: int) -> Dict[str, Any]:
        """Удалить пользователя и его историю"""
        self.session = aiohttp.ClientSession()
        payload = {
            "admin_id": admin_id,
            "user_id": user_id
        }
        try:
            if debug_mode:
                logger.info(f"Удаление пользователя {user_id}")
            async with self.session.delete(f"{self.base_url}/admin/delete-user", json=payload) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def create_promo_code(self, admin_id: int, code: str, max_uses: int, free_messages: int) -> Dict[str, Any]:
        """Создать промокод"""
        self.session = aiohttp.ClientSession()
        payload = {
            "admin_id": admin_id,
            "code": code,
            "max_uses": max_uses,
            "free_messages": free_messages
        }
        try:
            if debug_mode:
                logger.info(f"Создание промокода: {code}")
            async with self.session.post(f"{self.base_url}/admin/promo", json=payload) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None

    @handle_errors_async_method
    async def redeem_promo_code(self, user_id: int, code: str) -> Dict[str, Any]:
        """Активировать промокод"""
        self.session = aiohttp.ClientSession()
        payload = {
            "user_id": user_id,
            "code": code
        }
        try:
            if debug_mode:
                logger.info(f"Активация промокода {code} для {user_id}")
            async with self.session.post(f"{self.base_url}/promo/redeem", json=payload) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.session.close()
            self.session = None
