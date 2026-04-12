"""Админ панель"""

from aiogram.types import (
    Message,
    CallbackQuery,
    BufferedInputFile
)
from aiogram.fsm.context import FSMContext
from loguru import logger

from config import texts
from services.api_requests import api_client
from services.decorators import handle_resolver_errors
from services.states import StateMachine
from services.resolvers.keyboards import (
    get_back_to_admin_menu_keyboard,
    get_menu_keyboard,
    get_admin_menu_keyboard
)


async def _show_admin_menu(message: Message, user_id: int, state: FSMContext):
    """Показывает главное меню админки"""
    response = await api_client.check_admin_rights(user_id)
    if not response.get("is_admin"):
        await message.answer(
            texts.ADMIN_PANEL_AUTH_FAIL,
            reply_markup=get_menu_keyboard()
        )
        return
    await state.set_state(StateMachine.admin_main_menu)
    await message.answer(
        texts.ADMIN_PANEL_WELCOME,
        reply_markup=get_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_admin_menu(message: Message, state: FSMContext):
    """Показывает админ-панель (вызов через команду /admin)"""
    user_id = message.from_user.id
    await _show_admin_menu(message, user_id, state)


@handle_resolver_errors
async def resolve_admin_back(callback: CallbackQuery, state: FSMContext):
    """Возврат в меню админки (вызов через кнопку)"""
    await callback.answer()
    user_id = callback.from_user.id
    await _show_admin_menu(callback.message, user_id, state)


@handle_resolver_errors
async def resolve_admin_exit(callback: CallbackQuery, state: FSMContext):
    """Выход из админки"""
    await callback.answer()
    await state.clear()
    await callback.message.answer(
        texts.ADMIN_PANEL_OUTCOME,
        reply_markup=get_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_user_info_request(callback: CallbackQuery, state: FSMContext):
    """Запрос ID пользователя для получения информации"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_user_id_for_info)
    await callback.message.answer(
        texts.ADMIN_WAIT_USER_ID,
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_user_info_process(message: Message, state: FSMContext):
    """Получение информации о пользователе"""
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(texts.ADMIN_PARSE_USER_ID_ERROR)
        return

    admin_id = message.from_user.id
    response = await api_client.get_user_info(admin_id, user_id)
    keyboard = get_back_to_admin_menu_keyboard()

    if response.get("data"):
        data = response["data"]
        info_text = texts.ADMIN_FUNC_USER_INFO.format(
            user_id=user_id, active_subscriber=data.get('active_subscriber', False),
            subscription_end=data.get('subscription_end', False),
            free_messages=data.get('free_messages', 0),
            day_limit=data.get('day_limit', 0), is_admin=data.get('is_admin', False)
        )
        await message.answer(info_text, reply_markup=keyboard)
    else:
        error_msg = response.get('error', 'Unknown error')
        await message.answer(
            texts.ADMIN_ERROR_USER_ID.format(error_msg=error_msg), reply_markup=keyboard
        )
    await state.set_state(StateMachine.admin_main_menu)


# === Обработка SET-USER-OPTIONS === #

@handle_resolver_errors
async def resolve_options_request(callback: CallbackQuery, state: FSMContext):
    """Запрос ID пользователя для изменения параметров"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_user_id_for_options)
    await callback.message.answer(
        texts.ADMIN_WAIT_USER_ID,
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_options_user_id(message: Message, state: FSMContext):
    """Сохраняет ID и запрашивает настройки"""
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(texts.ADMIN_PARSE_USER_ID_ERROR)
        return
    await state.update_data(target_user_id=user_id)
    await state.set_state(StateMachine.admin_waiting_options_data)
    await message.answer(
        texts.ADMIN_OPTIONS_WAIT_DATA.format(user_id=user_id),
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_options_data(message: Message, state: FSMContext):
    """Парсит и применяет настройки"""
    data = await state.get_data()
    target_user_id = data.get("target_user_id")
    keyboard = get_back_to_admin_menu_keyboard()
    try:
        options = {}
        for pair in message.text.split():
            key, value = pair.split("=")
            if key in ("premium", "is_admin", "garbage_flag"):
                options[key] = value.lower() in ("true", "1", "yes")
            elif key in ("free_messages", "day_limit"):
                options[key] = int(value)
            else:
                await message.answer(
                    texts.ADMIN_OPTIONS_UNKNOWN_FIELD.format(key=key),
                    reply_markup=keyboard
                )
                return
        if not options:
            await message.answer(texts.ADMIN_OPTIONS_EMPTY,
                                 reply_markup=keyboard)
            return
    except ValueError as e:
        logger.error(f"Ошибка парсинга: {e}")
        await message.answer(texts.ADMIN_OPTIONS_EMPTY,
                             reply_markup=keyboard)
        return
    admin_id = message.from_user.id
    response = await api_client.set_user_options(admin_id, target_user_id, options)
    if response.get("success"):
        await message.answer(
            texts.ADMIN_OPTIONS_SUCCESS.format(
                target_user_id=target_user_id,
                message=response.get('message')
            ),
            reply_markup=keyboard
        )
    else:
        error_msg = response.get('message', 'Unknown error')
        await message.answer(
            texts.ADMIN_OPTIONS_ERROR.format(error_msg=error_msg),
            reply_markup=keyboard
        )
    await state.set_state(StateMachine.admin_main_menu)


@handle_resolver_errors
async def resolve_all_users(callback: CallbackQuery, state: FSMContext):
    """Получает список всех пользователей и отправляет файлом"""
    await callback.answer()
    admin_id = callback.from_user.id
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
            caption=texts.ADMIN_ALL_USERS_CAPTION.format(count=count),
            reply_markup=get_back_to_admin_menu_keyboard()
        )
    else:
        error_msg = response.get('error', 'Unknown error')
        await callback.message.answer(
            texts.ADMIN_ALL_USERS_ERROR.format(error_msg=error_msg)
        )
    await state.set_state(StateMachine.admin_main_menu)


@handle_resolver_errors
async def resolve_delete_user_request(callback: CallbackQuery, state: FSMContext):
    """Запрос ID пользователя для удаления"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_user_id_for_delete)
    await callback.message.answer(
        texts.ADMIN_DELETE_USER_WAIT,
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_delete_user_process(message: Message, state: FSMContext):
    """Удаление пользователя по ID"""
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(texts.ADMIN_PARSE_USER_ID_ERROR)
        return

    admin_id = message.from_user.id
    keyboard = get_back_to_admin_menu_keyboard()
    response = await api_client.delete_user(admin_id, user_id)

    if response.get("success"):
        deleted = response.get("messages_deleted", 0)
        await message.answer(
            texts.ADMIN_DELETE_USER_SUCCESS.format(
                user_id=user_id, deleted=deleted
            ),
            reply_markup=keyboard
        )
    else:
        await message.answer(
            response.get("error", "Unknown error"),
            reply_markup=keyboard
        )
    await state.set_state(StateMachine.admin_main_menu)


@handle_resolver_errors
async def resolve_create_promo_request(callback: CallbackQuery, state: FSMContext):
    """Запрос данных для создания промокода"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_promo_data)
    await callback.message.answer(
        texts.ADMIN_CREATE_PROMO_WAIT_DATA,
        reply_markup=get_back_to_admin_menu_keyboard(),
        parse_mode="HTML"
    )


@handle_resolver_errors
async def resolve_create_promo_process(message: Message, state: FSMContext):
    """Парсит данные и создаёт промокод"""
    keyboard = get_back_to_admin_menu_keyboard()
    parts = message.text.strip().split()

    if len(parts) != 3:
        await message.answer(
            texts.ADMIN_CREATE_PROMO_FORMAT_ERROR,
            reply_markup=keyboard
        )
        return
    code = parts[0]
    try:
        max_uses = int(parts[1])
        free_messages = int(parts[2])
    except ValueError:
        await message.answer(
            texts.ADMIN_CREATE_PROMO_PARSE_ERROR,
            reply_markup=keyboard
        )
        return

    admin_id = message.from_user.id
    response = await api_client.create_promo_code(admin_id, code, max_uses, free_messages)

    if response.get("success"):
        await message.answer(
            texts.ADMIN_CREATE_PROMO_SUCCESS.format(
                code=code, max_uses=max_uses, free_messages=free_messages
            ),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            response.get("error", "Unknown error"),
            reply_markup=keyboard
        )
    await state.set_state(StateMachine.admin_main_menu)


@handle_resolver_errors
async def resolve_send_message_request(callback: CallbackQuery, state: FSMContext):
    """ Отправка сообщения пользователю Запрос ID и текста сообщения"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_send_message)
    await callback.message.answer(
        texts.ADMIN_SEND_MESSAGE_WAIT,
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_send_message_process(message: Message, state: FSMContext):
    """Отправка сообщения пользователю Парсим ID + текст и отправляем"""
    keyboard = get_back_to_admin_menu_keyboard()
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            texts.ADMIN_SEND_MESSAGE_FORMAT_ERROR,
            reply_markup=keyboard
        )
        return

    try:
        user_id = int(parts[0])
    except ValueError:
        await message.answer(
            texts.ADMIN_SEND_MESSAGE_PARSE_ERROR,
            reply_markup=keyboard
        )
        return

    admin_id = message.from_user.id
    response = await api_client.send_message_to_user(admin_id, user_id, parts[1])

    if response.get("success"):
        await message.answer(response.get("message", "OK"), reply_markup=keyboard)
    else:
        await message.answer(response.get("error", "Unknown error"), reply_markup=keyboard)
    await state.set_state(StateMachine.admin_main_menu)


@handle_resolver_errors
async def resolve_broadcast_request(callback: CallbackQuery, state: FSMContext):
    """Массовая рассылка Запрос процента и текста"""
    await callback.answer()
    await state.set_state(StateMachine.admin_waiting_broadcast)
    await callback.message.answer(
        texts.ADMIN_BROADCAST_WAIT,
        reply_markup=get_back_to_admin_menu_keyboard()
    )


@handle_resolver_errors
async def resolve_broadcast_process(message: Message, state: FSMContext):
    """Массовая рассылка Парсим процент + текст и рассылаем"""
    keyboard = get_back_to_admin_menu_keyboard()
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            texts.ADMIN_BROADCAST_FORMAT_ERROR,
            reply_markup=keyboard
        )
        return
    try:
        percentage = int(parts[0])
    except ValueError:
        await message.answer(
            texts.ADMIN_BROADCAST_PARSE_ERROR,
            reply_markup=keyboard
        )
        return
    if percentage < 1 or percentage > 100:
        await message.answer(
            texts.ADMIN_BROADCAST_RANGE_ERROR,
            reply_markup=keyboard
        )
        return

    admin_id = message.from_user.id
    response = await api_client.broadcast(admin_id, parts[1], percentage)

    if response.get("success"):
        total = response.get("total", 0)
        attempted = response.get("attempted", 0)
        sent = response.get("sent", 0)
        await message.answer(
            texts.ADMIN_BROADCAST_SUCCESS.format(
                total=total, attempted=attempted, sent=sent
            ),
            reply_markup=keyboard
        )
    else:
        await message.answer(response.get("error", "Unknown error"), reply_markup=keyboard)
    await state.set_state(StateMachine.admin_main_menu)
