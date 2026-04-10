from typing import Any
import aiohttp
from loguru import logger
from config.config import debug_mode, BASE_URL
from services.decorators import handle_api_errors


class APIClient:
    """Клиент для работы с API сервера"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url: str):
        if not hasattr(self, '_initialized'):
            self.base_url = url
            self._session = None
            self._initialized = True

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        "Закрывает aiohttp сессию"
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    @handle_api_errors
    async def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        session = await self._get_session()
        url = f"{self.base_url}{path}"
        if debug_mode:
            logger.debug(f"{method} {url}")
        async with session.request(method, url, **kwargs) as response:
            data = await response.json()
            if response.status != 200:
                logger.error(f"{method} {url} -> {response.status}: {data}")
            return data

    # Обработка запросов пользователя #

    async def send_message(self, user_id: int, text: str) -> dict[str, Any]:
        "Добавить сообщение пользователя в диалог и получить ответ от бота"
        return await self._request("POST", "/user/send-message",
                                   json={"user_id": user_id, "content": text}
                                  )

    async def get_user_stats(self, telegram_id: int) -> dict[str, Any]:
        "Получить статистику пользователя для личного кабинета"
        return await self._request("POST", "/user/info", 
                                   json={"user_id": telegram_id}
                                  )

    async def get_about(self) -> dict[str, Any]:
        "Получить информацию о боте"
        return await self._request("GET", "/about")

    async def redeem_promo_code(self, user_id: int, code: str) -> dict[str, Any]:
        return await self._request("POST", "/promo/redeem",
            json={"user_id": user_id, "code": code}
        )

    # === Подписка прайс и активация === #

    async def get_subscription_status(self, telegram_id: int) -> dict[str, Any]:
        return await self._request("GET", "/subscription/status",
            params={"telegram_id": telegram_id}
        )

    async def get_pricing_stars(self) -> dict[str, Any]:
        return await self._request("GET", "/subscription/pricing-stars")

    async def activate_subscription(
        self, telegram_id: int, plan: str, telegram_payment_id: str, amount: int, provider: str,
    ) -> dict[str, Any]:
        return await self._request("POST", "/subscription/activate", json={
            "telegram_id": telegram_id, 
            "plan": plan,
            "telegram_payment_id": telegram_payment_id,
            "amount": amount,
            "provider": provider
        })

    # === Admin === #

    async def check_admin_rights(self, admin_id: int) -> dict[str, Any]:
        return await self._request("GET", "/admin/check_rights",
            params={"admin_id": admin_id}
        )

    async def get_user_info(self, admin_id: int, user_id: int) -> dict[str, Any]:
        return await self._request("POST", "/admin/get-info", json={
            "admin_id": admin_id, "user_id": user_id
        })

    async def set_user_options(
        self, admin_id: int, user_id: int, options: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._request("PATCH", "/admin/set-options", json={
            "admin_id": admin_id, "user_id": user_id, "options": options,
        })

    async def get_all_users(self, admin_id: int) -> dict[str, Any]:
        return await self._request("GET", "/admin/users", params={"admin_id": admin_id})

    async def delete_user(self, admin_id: int, user_id: int) -> dict[str, Any]:
        return await self._request("DELETE", "/admin/delete-user",
            json={"admin_id": admin_id, "user_id": user_id}
        )

    async def create_promo_code(
        self, admin_id: int, code: str, max_uses: int, free_messages: int
    ) -> dict[str, Any]:
        return await self._request("POST", "/admin/promo", json={
            "admin_id": admin_id, "code": code, "max_uses": max_uses,
            "free_messages": free_messages
        })

    async def send_message_to_user(
        self, admin_id: int, user_id: int, message: str
    ) -> dict[str, Any]:
        return await self._request("POST", "/admin/send-message", json={
            "admin_id": admin_id, "user_id": user_id, "message": message
        })

    async def broadcast(
        self, admin_id: int, message: str, percentage: int
    ) -> dict[str, Any]:
        return await self._request("POST", "/admin/broadcast", json={
            "admin_id": admin_id, "message": message, "percentage": percentage
        })


api_client = APIClient(BASE_URL)
