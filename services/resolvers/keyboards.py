"""Клавиатуры для обработчиков"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from config.config import PLAN_LABELS

def get_back_to_admin_menu_keyboard():
    """Клавиатура с кнопкой 'Назад в меню'"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад в меню", callback_data="admin_back_to_menu")]
    ])


def get_menu_keyboard():
    """Постоянная подклавиатурная кнопка Меню"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Меню 📊")]],
        resize_keyboard=True,
        input_field_placeholder="Напиши что-нибудь..."
    )


def get_admin_menu_keyboard():
    """Клавиатура с админскими кнопками"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить профиль user_id", callback_data="admin_user_info")],
        [InlineKeyboardButton(text="Изменить настройки user_id", callback_data="admin_set_options")],
        [InlineKeyboardButton(text="User_id всех пользователей", callback_data="admin_all_users")],
        [InlineKeyboardButton(text="Удалить пользователя", callback_data="admin_delete_user")],
        [InlineKeyboardButton(text="Создать промокод", callback_data="admin_create_promo")],
        [InlineKeyboardButton(text="Отправить сообщение", callback_data="admin_send_message")],
        [InlineKeyboardButton(text="Массовая рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="Выход", callback_data="admin_exit")]
    ])


def get_subscription_keyboard(prices: dict) -> InlineKeyboardMarkup:
    """Клавиатура выбора плана подписки"""
    buttons = []
    for plan, label in PLAN_LABELS.items():
        sub = prices.get(plan)
        if sub:
            buttons.append([
                InlineKeyboardButton(
                    text=label,
                    callback_data=f"sub_plan_{plan}"
                )
            ])
    buttons.append([
        InlineKeyboardButton(text="Отмена", callback_data="sub_cancel")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_method_keyboard(plan: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора способа оплаты (пока только Stars)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатить звёздами ⭐",
                callback_data=f"sub_pay_stars_{plan}"
            )
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="sub_back_to_plans")
        ],
    ])


def get_lk_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура личного кабинета"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Показать прогресс отношений", callback_data="menu_relationship")
        ],
        [InlineKeyboardButton(text="Ввести промокод", callback_data="menu_promo")],
        [InlineKeyboardButton(text="Купить подписку", callback_data="menu_buy")],
    ])
