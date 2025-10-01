from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.resolver import resolve_model_message, resolve_hello

router = Router()


def setup_router():
    """Настройка роутера с внедрением зависимостей"""

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        """Обработчик команды /start"""
        await resolve_hello(message)

    @router.message(Command("help"))
    async def cmd_help(message: Message):
        """Обработчик команды /help"""
        await resolve_hello(message)

    @router.message()
    async def handle_message(message: Message):
        """Обработчик всех текстовых сообщений"""
        await resolve_model_message(message)

    return router