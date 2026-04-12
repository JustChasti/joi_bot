"""Типовые сообщения пользователя"""

from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext
from loguru import logger

from config import texts
from services.api_requests import api_client
from services.decorators import handle_resolver_errors
from services.resolvers.keyboards import (
    get_menu_keyboard,
    get_lk_menu_keyboard
)


@handle_resolver_errors
async def resolve_model_message(message: Message):
    """Основная функция и логика - отправка сообщений и получение ответа от сервера"""
    user_id = message.from_user.id
    text = message.text

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    response_data = await api_client.send_message(user_id, text)

    if not response_data.get("success", True):
        code = response_data.get("message", "")

        if code == "day_limit_exceeded":
            await message.answer(
                texts.END_DAY_LIMIT,
                reply_markup=get_menu_keyboard()
            )
        elif code == "free_messages_exhausted":
            await message.answer(
                texts.FREE_MESSAGES_EXHAUSTED,
                reply_markup=get_menu_keyboard()
            )
        else:
            logger.error(f"resolve_model_message: ошибка бэкенда для {user_id}: {code}")
            await message.answer(
                texts.SERVICE_UNAVAILABLE,
                reply_markup=get_menu_keyboard()
            )
        return

    answer = response_data.get("message", "")
    if len(answer) > 4000:
        answer = answer[:4000] + "\n...\n(ответ обрезан)"
    await message.answer(answer, parse_mode="HTML", reply_markup=get_menu_keyboard())


@handle_resolver_errors
async def resolve_hello(message: Message):
    """Отправка приветственного сообщения"""
    await message.answer(
        texts.HELLO_TEXT,
        parse_mode="HTML",
        reply_markup=get_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_unsupported_content(message: Message):
    """Обработка нетекстовых сообщений (фото, файлы, голосовые и т.д.)"""
    content_type_names = {
        "photo": "фотографии",
        "voice": "голосовые сообщения",
        "audio": "аудио файлы",
        "video": "видео",
        "video_note": "видеосообщения",
        "document": "файлы",
        "sticker": "стикеры",
        "animation": "GIF-анимации",
        "location": "геолокацию",
        "contact": "контакты"
    }

    content_type = message.content_type
    content_name = content_type_names.get(content_type, "такой тип сообщений")

    await message.answer(
        texts.UNSUPORTED_MESSAGE.format(content_name=content_name),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard()
    )
@handle_resolver_errors
async def resolve_about(message: Message):
    """Команда /about — информация о боте"""
    response = await api_client.get_about()

    if response.get("success"):
        await message.answer(
            response.get("text", ""), parse_mode="HTML", reply_markup=get_menu_keyboard()
        )
    else:
        await message.answer(
            texts.ABOUT_LOAD_ERROR, reply_markup=get_menu_keyboard()
        )


# личный кабинет
RELATIONSHIP_STAGE_LABELS = {
    "acquaintance": "Знакомство",
    "friend": "Дружба",
    "romantic": "Отношения",
}

# Порядок стадий и их позиция на шкале (0.0 - 1.0)
RELATIONSHIP_STAGES_ORDER = ["acquaintance", "friend", "romantic"]


def build_relationship_progress(stage: str) -> str:
    """Строит визуальный прогресс-бар отношений"""
    stages = RELATIONSHIP_STAGES_ORDER
    total_bars = 10  # длина шкалы

    try:
        current_index = stages.index(stage)
    except ValueError:
        current_index = 0

    # Прогресс: для 3 стадий → 0=33%, 1=66%, 2=100%
    progress = (current_index + 1) / len(stages)
    filled = round(total_bars * progress)
    empty = total_bars - filled

    progress_bar = "█" * filled + "░" * empty

    # Собираем текст с метками стадий
    lines = []
    for i, s in enumerate(stages):
        label = RELATIONSHIP_STAGE_LABELS.get(s, s)
        if i == current_index:
            lines.append(f"  ➤ {label}")
        elif i < current_index:
            lines.append(f"  ✓ {label}")
        else:
            lines.append(f"  ○ {label}")

    stage_list = "\n".join(lines)

    return texts.LK_RELATIONSHIP_PROGRESS.format(
        progress_bar=progress_bar,
        progress_percent=int(progress * 100),
        stage_list=stage_list,
    )


@handle_resolver_errors
async def resolve_menu_button(message: Message, state: FSMContext):
    """Обработка нажатия кнопки 'Меню' — показ личного кабинета"""
    # Сбрасываем FSM, чтобы не конфликтовать с другими состояниями
    await state.clear()
    user_id = message.from_user.id
    response = await api_client.get_user_stats(user_id)

    if not response or not response.get("success"):
        await message.answer(
            texts.LK_LOAD_ERROR,
            reply_markup=get_menu_keyboard()
        )
        return

    # Парсим данные
    data = response.get("data", {})
    active_sub = data.get("active_subscriber", False)
    sub_end = data.get("subscription_end", "")
    free_messages = data.get("free_messages", 0)

    if active_sub and sub_end:
        sub_status = texts.LK_SUB_ACTIVE.format(sub_end=sub_end)
    else:
        sub_status = texts.LK_SUB_INACTIVE

    text = texts.LK_PROFILE.format(
        sub_status=sub_status,
        free_messages=free_messages,
    )

    keyboard = get_lk_menu_keyboard()
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@handle_resolver_errors
async def resolve_menu_relationship(callback: CallbackQuery):
    """Показать прогресс отношений"""
    await callback.answer()
    user_id = callback.from_user.id
    response = await api_client.get_user_stats(user_id)

    if not response or not response.get("success"):
        await callback.message.answer(
            texts.LK_LOAD_ERROR,
            reply_markup=get_menu_keyboard()
        )
        return

    data = response.get("data", {})
    stage = data.get("relationship_stage", "acquaintance")
    progress_text = build_relationship_progress(stage)
    await callback.message.answer(
        progress_text, parse_mode="HTML", reply_markup=get_menu_keyboard()
    )
