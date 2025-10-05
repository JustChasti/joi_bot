from aiogram.types import Message
from loguru import logger

from config.config import url_send_mesage, text_hello
from services.api_requests import APIClient
from services.decorators import handle_errors_async


@handle_errors_async
async def resolve_model_message(message: Message):
    """Обработка сообщений непосредственно к ЛЛМ"""
    user_id = message.from_user.id
    text = message.text
    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    api_client = APIClient(url_send_mesage)
    response_data = await api_client.send_message(user_id, text)
    answer = response_data["text"]
    if len(answer) > 4000:
        answer = answer[:4000] + "\n...\n(ответ обрезан)"
    await message.answer(
        answer,
        parse_mode="HTML"
    )

@handle_errors_async
async def resolve_hello(message: Message):
    """ Читает заготовленный файл и отправляет пользователю"""
    text_file = text_hello
    content = ""
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {text_file}: {e}", exc_info=True)
        content = "Привет, Это Джой!\n Напиши мне что и получи новый опыт)"
    help_text = f"{content}\n\n📌 Доступные команды:\n /start /help - Показать эту справку"
    await message.answer(
        help_text,
        parse_mode=None
    )
