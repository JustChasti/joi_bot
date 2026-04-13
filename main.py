import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher

from config import config
from services.handlers import setup_router
from services.api_requests import api_client


async def main():
    """Запуск"""
    logger.info("Запуск бота...")
    logger.info(f"Конфигурация загружена. Server URL: {config.host}")
    bot = Bot(token=config.token)
    dp = Dispatcher()
    dp.include_router(setup_router())
    try:
        # Запуск polling
        logger.info("Бот запущен!")
        await dp.start_polling(bot)
    finally:
        api_client.close()
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.exception(f"Критическая ошибка: {e}")
