from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from services.states import StateMachine
from services.resolver import (
    resolve_hello,
    resolve_model_message,
    resolve_admin_menu,
    resolve_user_info_request,
    resolve_user_info_process,
    resolve_options_request,
    resolve_options_user_id,
    resolve_options_data,
    resolve_all_users,
    resolve_admin_back,
    resolve_admin_exit
)

router = Router()


def setup_router():
    """Настройка обработчиков сообщений"""
    @router.message(Command("start"))
    async def cmd_start(message: Message):
        await resolve_hello(message)

    @router.message(Command("help"))
    async def cmd_help(message: Message):
        await resolve_hello(message)

    @router.message(Command("admin"))
    async def cmd_admin(message: Message, state: FSMContext):
        await resolve_admin_menu(message, state)

    # === АДМИН ПАНЕЛЬ === #

    @router.callback_query(F.data == "admin_user_info", StateMachine.admin_main_menu)
    async def admin_user_info(callback: CallbackQuery, state: FSMContext):
        await resolve_user_info_request(callback, state)

    @router.callback_query(F.data == "admin_set_options", StateMachine.admin_main_menu)
    async def admin_set_options(callback: CallbackQuery, state: FSMContext):
        await resolve_options_request(callback, state)

    @router.callback_query(F.data == "admin_all_users", StateMachine.admin_main_menu)
    async def admin_all_users(callback: CallbackQuery, state: FSMContext):
        await resolve_all_users(callback, state)

    @router.callback_query(F.data == "admin_back_to_menu")
    async def admin_back(callback: CallbackQuery, state: FSMContext):
        await resolve_admin_back(callback, state)

    @router.callback_query(F.data == "admin_exit")
    async def admin_exit(callback: CallbackQuery, state: FSMContext):
        await resolve_admin_exit(callback, state)

    @router.message(StateMachine.admin_waiting_user_id_for_info)
    async def admin_process_user_id_info(message: Message, state: FSMContext):
        await resolve_user_info_process(message, state)

    @router.message(StateMachine.admin_waiting_user_id_for_options)
    async def admin_process_user_id_options(message: Message, state: FSMContext):
        await resolve_options_user_id(message, state)

    @router.message(StateMachine.admin_waiting_options_data)
    async def admin_process_options_data(message: Message, state: FSMContext):
        await resolve_options_data(message, state)

    # === ОБЫЧНОЕ ОБЩЕНИЕ (последний обработчик!) === #

    @router.message()
    async def handle_message(message: Message):
        await resolve_model_message(message)

    return router
