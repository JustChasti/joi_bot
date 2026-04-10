import functools
from typing import Callable
from loguru import logger
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
import aiohttp
from config.config import service_unavailable_text


# 1. Декоратор для обычной функции
def handle_errors(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в обычных функциях
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return {"success": False, "error": str(e)}
    return wrapper


# 2. Декоратор для метода класса
def handle_errors_method(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок в методах класса
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return {"success": False, "error": str(e)}
    return wrapper


def handle_resolver_errors(func: Callable) -> Callable:
    """Декоратор для resolver'ов — ловит непредвиденные ошибки и уведомляет пользователя"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Ошибка в {func.__name__}: {e}")
            event = args[0] if args else None
            if isinstance(event, Message):
                await event.answer(service_unavailable_text)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(service_unavailable_text)
            elif isinstance(event, PreCheckoutQuery):
                await event.answer(ok=False, error_message=service_unavailable_text)
    return wrapper


def handle_api_errors(func: Callable) -> Callable:
    """Декоратор для методов APIClient — ловит ошибки aiohttp"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError as e:
            logger.error(f"API error in {func.__name__}: {e}")
            return {"success": False, "error": "Connection error"}
    return wrapper
