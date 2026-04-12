"""Подписка и платежи"""
from typing import Callable, Awaitable, Any
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery
from loguru import logger

from config.config import PLAN_LABELS
from config import texts
from services.api_requests import api_client
from services.decorators import handle_resolver_errors
from services.states import StateMachine
from services.resolvers.keyboards import (
    get_menu_keyboard,
    get_subscription_keyboard,
    get_payment_method_keyboard,
)


async def _show_subscription_menu(
        user_id: int, state: FSMContext, send_fn: Callable[..., Awaitable[Any]]):
    """Общая логика показа меню подписки"""
    status = await api_client.get_subscription_status(user_id)
    pricing = await api_client.get_pricing_stars()
    if not pricing.get("success") or not status.get("success"):
        logger.error(
        f"не удалось получить данные для {user_id}:"
        f"pricing={pricing.get('success')}, status={status.get('success')}"
        )
        await send_fn(texts.SUB_LOAD_ERROR)
        return

    if status.get("active"):
        end_date = status.get("end_date", "")
        plan_label = PLAN_LABELS.get(status.get("plan"))
        header = texts.SUB_HEADER_ACTIVE.format(
            plan_label=plan_label, end_date=end_date
        )
    else:
        header = texts.SUB_HEADER_INACTIVE

    await state.set_state(StateMachine.subscription_menu)
    await send_fn(
        header,
        reply_markup=get_subscription_keyboard(pricing["prices"]),
        parse_mode="HTML"
    )


@handle_resolver_errors
async def resolve_buy_command(message: Message, state: FSMContext):
    """Показывает меню подписки по команде /buy"""
    await _show_subscription_menu(message.from_user.id, state, message.answer)


@handle_resolver_errors
async def resolve_subscription_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена — выход из меню подписки"""
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(texts.SUB_CANCEL)


@handle_resolver_errors
async def resolve_subscription_plan_selected(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал план — показываем выбор способа оплаты"""
    await callback.answer()
    plan = callback.data.replace("sub_plan_", "")

    await state.clear()

    await callback.message.edit_text(
        texts.SUB_PLAN_SELECTED.format(plan=plan),
        reply_markup=get_payment_method_keyboard(plan),
        parse_mode="HTML"
    )


@handle_resolver_errors
async def resolve_subscription_back_to_plans(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору плана"""
    await callback.answer()
    await _show_subscription_menu(callback.from_user.id, state, callback.message.edit_text)


@handle_resolver_errors
async def resolve_pay_stars(callback: CallbackQuery, state: FSMContext):
    """Пользователь выбрал оплату звёздами — отправляем инвойс"""
    await callback.answer()
    await state.clear()
    plan = callback.data.replace("sub_pay_stars_", "")
    pricing = await api_client.get_pricing_stars()

    if not pricing.get("success"):
        logger.error(f"resolve_pay_stars: не удалось получить цены: {pricing.get('error')}")
        await callback.message.answer(
            texts.SUB_PAY_STARS_PRICES_ERROR, reply_markup=get_menu_keyboard()
        )
        return

    stars_amount = pricing["prices"].get(plan)
    if not stars_amount:
        await callback.message.answer(
            texts.SUB_PAY_STARS_UNKNOWN_PLAN, reply_markup=get_menu_keyboard()
        )
        return

    await callback.message.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=texts.SUB_INVOICE_TITLE.format(plan=plan),
        description=texts.SUB_INVOICE_DESCRIPTION.format(plan=plan),
        payload=plan,
        currency="XTR",
        prices=[LabeledPrice(label=texts.SUB_INVOICE_LABEL.format(plan=plan), amount=stars_amount)],
    )


@handle_resolver_errors
async def resolve_pre_checkout(query: PreCheckoutQuery):
    """Telegram требует ответить в течение 10 секунд"""
    user_id = query.from_user.id
    try:
        status = await api_client.get_subscription_status(user_id)
        if not status.get("success"):
            logger.error(f"resolve_pre_checkout: {user_id}: {status.get('error')}")
            await query.answer(
                ok=False,
                error_message=texts.SUB_PRE_CHECKOUT_SERVICE_ERROR
            )
            return
        await query.answer(ok=True)

    except (OSError, ValueError, TypeError) as e:
        logger.error(f"resolve_pre_checkout: неожиданная ошибка для {user_id}: {e}")
        await query.answer(
            ok=False,
            error_message=texts.SUB_PRE_CHECKOUT_ERROR
        )


@handle_resolver_errors
async def resolve_successful_payment(message: Message, state: FSMContext):
    """Оплата прошла — активируем подписку на бэкенде"""
    payment = message.successful_payment
    plan = payment.invoice_payload
    result = await api_client.activate_subscription(
        telegram_id=message.from_user.id,
        plan=plan,
        telegram_payment_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount,
        provider="telegram"
    )

    await state.clear()

    if result.get("success"):
        end_date = result.get("end_date", "")
        plan_label = PLAN_LABELS.get(plan, plan)
        await message.answer(
            texts.SUB_PAYMENT_SUCCESS.format(
                plan_label=plan_label, end_date=end_date
            ),
            parse_mode="HTML",
            reply_markup=get_menu_keyboard()
        )
    else:
        error = result.get("error", "Unknown error")
        logger.error(f"resolve_successful_payment: failed для {message.from_user.id}: {error}")
        await message.answer(
            texts.SUB_PAYMENT_ACTIVATION_ERROR,
            reply_markup=get_menu_keyboard()
        )


@handle_resolver_errors
async def resolve_menu_buy(callback: CallbackQuery, state: FSMContext):
    """Переход к покупке подписки из меню"""
    await callback.answer()
    await _show_subscription_menu(callback.from_user.id, state, callback.message.answer)
