"""Работа с промокодами"""

from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext

from config import texts
from services.api_requests import api_client
from services.decorators import handle_resolver_errors
from services.states import StateMachine
from services.resolvers.keyboards import (
    get_menu_keyboard
)


@handle_resolver_errors
async def resolve_promo_command(message: Message, state: FSMContext):
    """Команда /promo — просит ввести код"""
    await state.set_state(StateMachine.promo_waiting_code)
    await message.answer(texts.PROMO_WAIT_CODE)


@handle_resolver_errors
async def resolve_promo_code_entered(message: Message, state: FSMContext):
    """Пользователь ввёл промокод — активируем"""
    code = message.text.strip()
    user_id = message.from_user.id

    response = await api_client.redeem_promo_code(user_id, code)

    await state.clear()

    if response.get("success"):
        free = response.get("free_messages", 0)
        await message.answer(
            texts.PROMO_SUCCESS.format(free=free),
            reply_markup=get_menu_keyboard()
        )
    else:
        server_error = response.get("error", "")
        user_msg = texts.PROMO_ERROR_MESSAGES.get(server_error, texts.PROMO_UNKNOWN_ERROR)
        await message.answer(user_msg, reply_markup=get_menu_keyboard())


@handle_resolver_errors
async def resolve_menu_promo(callback: CallbackQuery, state: FSMContext):
    """Переход к вводу промокода из меню"""
    await callback.answer()
    await resolve_promo_command(callback.message, state)
