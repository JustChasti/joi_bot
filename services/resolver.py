from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BufferedInputFile
)
from aiogram.fsm.context import FSMContext
from loguru import logger

from config.config import base_url, text_hello
from services.api_requests import APIClient
from services.decorators import handle_errors_async
from services.states import StateMachine


def get_back_to_menu_keyboard():
    """Возвращает клавиатуру с кнопкой 'Назад в меню'"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад в меню", callback_data="admin_back_to_menu")]
    ])


# === Обработка КОМАНД ПОЛЬЗОВАТЕЛЯ === #
@handle_errors_async
async def resolve_model_message(message: Message):
    """Обработка сообщений непосредственно к ЛЛМ"""
    user_id = message.from_user.id
    text = message.text
    # Отправляем статус "печатает..."
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    api_client = APIClient(base_url)
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
    except (FileNotFoundError, OSError) as e:
        logger.error(f"Ошибка при чтении файла {text_file}: {e}", exc_info=True)
        content = "Привет, Это Джой!\n Напиши мне что и получи новый опыт)"
    help_text = f"{content}\n\n Доступные команды:\n /start /help - Показать эту справку"
    await message.answer(
        help_text,
        parse_mode=None
    )


@handle_errors_async
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
        f"Пока я не умею обрабатывать {content_name} \n\n"
        "Давай лучше пообщаемся текстовыми сообщениями! Напиши мне что-нибудь",
        parse_mode="HTML"
    )

# === Обработка АДМИН-ПАНЕЛИ === #

async def _show_admin_menu(user_id: int, message: Message, state: FSMContext):
    """Показывает главное меню админки"""
    api_client = APIClient(base_url)
    is_admin = await api_client.check_admin_rights(user_id)
    if not is_admin:
        await message.answer(
            "У вас нет прав администратора.\n\n"
            "Для получения прав администратора обратитесь к разработчикам бота.",
            parse_mode="HTML"
        )
        return
    await state.set_state(StateMachine.admin_main_menu)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить профиль user_id", callback_data="admin_user_info")],
        [InlineKeyboardButton(text="Изменить настройки user_id",
                              callback_data="admin_set_options")],
        [InlineKeyboardButton(text="User_id всех пользователей", callback_data="admin_all_users")],
        [InlineKeyboardButton(text="Выход", callback_data="admin_exit")]
    ])

    await message.answer(
        "Админ-панель\n\nВыберите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@handle_errors_async
async def resolve_admin_menu(message: Message, state: FSMContext):
    """Показывает админ-панель (вызов через команду /admin)"""
    user_id = message.from_user.id
    await _show_admin_menu(user_id, message, state)


@handle_errors_async
async def resolve_admin_back(callback: CallbackQuery, state: FSMContext):
    """Возврат в меню админки (вызов через кнопку)"""
    await callback.answer()
    user_id = callback.from_user.id
    await _show_admin_menu(user_id, callback.message, state)


@handle_errors_async
async def resolve_admin_exit(callback: CallbackQuery, state: FSMContext):
    """Выход из админки"""
    await callback.answer()
    await state.clear()
    await callback.message.answer(
        "Вы вышли из админ-панели.\nМожете продолжить общение."
    )

# === Обработка GET-USER-INFO === #

@handle_errors_async
async def resolve_user_info_request(callback: CallbackQuery, state: FSMContext):
    """Запрос ID пользователя для получения информации"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_user_id_for_info)

    keyboard = get_back_to_menu_keyboard()
    await callback.message.answer(
        "Информация о пользователе\n\nВведите ID пользователя:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@handle_errors_async
async def resolve_user_info_process(message: Message, state: FSMContext):
    """Получение информации о пользователе"""
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Неверный формат ID. Введите число:")
        return

    admin_id = message.from_user.id
    api_client = APIClient(base_url)
    response = await api_client.get_user_info(admin_id, user_id)

    if response.get("data"):
        data = response["data"]
        info_text = (
            f"Информация о пользователе {user_id}\n\n"
            f"Premium: {data.get('premium', False)}\n"
            f"Бесплатных сообщений: {data.get('free_messages', 0)}\n"
            f"Осталось сообщений сегодня: {data.get('day_limit', 0)}\n"
            f"Admin: {data.get('is_admin', False)}"
        )
        keyboard = get_back_to_menu_keyboard()
        await message.answer(info_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        keyboard = get_back_to_menu_keyboard()
        error_msg = response.get('error', 'Unknown error')
        await message.answer(f"Ошибка получения информации о пользователе:\n{error_msg}",
                             reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(StateMachine.admin_main_menu)


# === Обработка SET-USER-OPTIONS === #

@handle_errors_async
async def resolve_options_request(callback: CallbackQuery, state: FSMContext):
    """Запрос ID пользователя для изменения параметров"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_user_id_for_options)
    keyboard = get_back_to_menu_keyboard()
    await callback.message.answer(
        "Изменение настроек\n\nВведите ID пользователя:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@handle_errors_async
async def resolve_options_user_id(message: Message, state: FSMContext):
    """Сохраняет ID и запрашивает настройки"""
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("Неверный формат ID. Введите число:")
        return
    await state.update_data(target_user_id=user_id)
    await state.set_state(StateMachine.admin_waiting_options_data)
    keyboard = get_back_to_menu_keyboard()
    await message.answer(
        f"Настройки для пользователя {user_id}\n\n"
        "Формат: premium=true free_messages=100 day_limit=50\n\n"
        "Доступные поля:\n"
        "premium (true/false)\n"
        "free_messages (число)\n"
        "is_admin (true/false)\n"
        "garbage_flag (true/false)\n"
        "day_limit (число)",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@handle_errors_async
async def resolve_options_data(message: Message, state: FSMContext):
    """Парсит и применяет настройки"""
    data = await state.get_data()
    target_user_id = data.get("target_user_id")
    keyboard = get_back_to_menu_keyboard()
    try:
        options = {}
        for pair in message.text.split():
            key, value = pair.split("=")
            if key in ("premium", "is_admin", "garbage_flag"):
                options[key] = value.lower() in ("true", "1", "yes")
            elif key in ("free_messages", "day_limit"):
                options[key] = int(value)
            else:
                await message.answer(f"Неизвестное поле: {key}",
                                     reply_markup=keyboard, parse_mode="HTML")
                return
        if not options:
            await message.answer("Не указано ни одного параметра",
                                 reply_markup=keyboard, parse_mode="HTML")
            return
    except ValueError as e:
        logger.error(f"Ошибка парсинга: {e}")
        await message.answer("Не указано ни одного параметра",
                             reply_markup=keyboard, parse_mode="HTML")
        return
    admin_id = message.from_user.id
    api_client = APIClient(base_url)
    response = await api_client.set_user_options(admin_id, target_user_id, options)
    if response.get("success"):
        await message.answer(
            f"Обновлены поля пользователя {target_user_id}, {response.get('message')}",
            reply_markup=keyboard, parse_mode="HTML"
        )
    else:
        error_msg = response.get('message', 'Unknown error')
        await message.answer(f"Ошибка обновления: {error_msg}",
                             reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(StateMachine.admin_main_menu)


# === Обработка GET-ALL-USERS === #

@handle_errors_async
async def resolve_all_users(callback: CallbackQuery, state: FSMContext):
    """Получает список всех пользователей и отправляет файлом"""
    await callback.answer()
    admin_id = callback.from_user.id
    api_client = APIClient(base_url)
    keyboard = get_back_to_menu_keyboard()
    response = await api_client.get_all_users(admin_id)
    if "users" in response:
        users = response["users"]
        count = response["count"]
        # Создаем текстовый файл
        users_text = ""
        for user_id in users:
            users_text += str(user_id) + "\n"
        file_content = users_text.encode('utf-8')
        file = BufferedInputFile(file_content, filename="users.txt")
        await callback.message.answer_document(
            document=file,
            caption=f"Всего пользователей: {count}",
            reply_markup=keyboard, parse_mode="HTML"
        )
    else:
        error_msg = response.get('error', 'Unknown error')
        await callback.message.answer(f"Ошибка получения списка: {error_msg}")
    await state.set_state(StateMachine.admin_main_menu)
