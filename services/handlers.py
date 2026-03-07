from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
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
    resolve_admin_exit,
    resolve_unsupported_content,
    resolve_buy_command,
    resolve_subscription_cancel,
    resolve_subscription_plan_selected,
    resolve_subscription_back_to_plans,
    resolve_pay_stars,
    resolve_pre_checkout,
    resolve_successful_payment,
    resolve_delete_user_request,
    resolve_delete_user_process,
    resolve_create_promo_request,
    resolve_create_promo_process,
    resolve_promo_command,
    resolve_promo_code_entered,
    resolve_about,
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

    @router.message(Command("about"))
    async def cmd_about(message: Message):
        await resolve_about(message)

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

    @router.callback_query(F.data == "admin_delete_user", StateMachine.admin_main_menu)
    async def admin_delete_user(callback: CallbackQuery, state: FSMContext):
        await resolve_delete_user_request(callback, state)

    @router.message(StateMachine.admin_waiting_user_id_for_delete)
    async def admin_process_delete_user(message: Message, state: FSMContext):
        await resolve_delete_user_process(message, state)

    @router.callback_query(F.data == "admin_create_promo", StateMachine.admin_main_menu)
    async def admin_create_promo(callback: CallbackQuery, state: FSMContext):
        await resolve_create_promo_request(callback, state)

    @router.message(StateMachine.admin_waiting_promo_data)
    async def admin_process_promo_data(message: Message, state: FSMContext):
        await resolve_create_promo_process(message, state)

# === ПРОМОКОД === #

    @router.message(Command("promo"))
    async def cmd_promo(message: Message, state: FSMContext):
        await resolve_promo_command(message, state)

    @router.message(StateMachine.promo_waiting_code)
    async def promo_code_entered(message: Message, state: FSMContext):
        await resolve_promo_code_entered(message, state)

# === ПОДПИСКА === #

    @router.message(Command("buy"))
    async def cmd_buy(message: Message, state: FSMContext):
        await resolve_buy_command(message, state)

    @router.callback_query(F.data == "sub_cancel")
    async def sub_cancel(callback: CallbackQuery, state: FSMContext):
        await resolve_subscription_cancel(callback, state)

    @router.callback_query(F.data == "sub_back_to_plans")
    async def sub_back_to_plans(callback: CallbackQuery, state: FSMContext):
        await resolve_subscription_back_to_plans(callback, state)

    @router.callback_query(F.data.startswith("sub_plan_"))
    async def sub_plan_selected(callback: CallbackQuery, state: FSMContext):
        await resolve_subscription_plan_selected(callback, state)

    @router.callback_query(F.data.startswith("sub_pay_stars_"))
    async def sub_pay_stars(callback: CallbackQuery, state: FSMContext):
        await resolve_pay_stars(callback, state)

    @router.pre_checkout_query()
    async def pre_checkout(query: PreCheckoutQuery):
        await resolve_pre_checkout(query)

    @router.message(F.successful_payment)
    async def successful_payment(message: Message, state: FSMContext):
        await resolve_successful_payment(message, state)

    # === ОБРАБОТКА НЕТЕКСТОВЫХ СООБЩЕНИЙ === #

    @router.message(F.photo)
    async def handle_photo(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.voice)
    async def handle_voice(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.audio)
    async def handle_audio(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.video)
    async def handle_video(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.video_note)
    async def handle_video_note(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.document)
    async def handle_document(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.sticker)
    async def handle_sticker(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.animation)
    async def handle_animation(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.location)
    async def handle_location(message: Message):
        await resolve_unsupported_content(message)

    @router.message(F.contact)
    async def handle_contact(message: Message):
        await resolve_unsupported_content(message)

    # === ОБЫЧНОЕ ОБЩЕНИЕ (последний обработчик!) === #

    @router.message()
    async def handle_message(message: Message):
        await resolve_model_message(message)

    return router
