from aiogram.fsm.state import State, StatesGroup


class StateMachine(StatesGroup):
    """Машина состояний для бота"""

    # === АДМИН ПАНЕЛЬ === #
    admin_main_menu = State()
    admin_waiting_user_id_for_info = State()
    admin_waiting_user_id_for_options = State()
    admin_waiting_options_data = State()
    admin_waiting_user_id_for_delete = State()
    admin_waiting_promo_data = State()

    # === ПОДПИСКА === #
    subscription_menu = State()  # пользователь в меню выбора плана

    # === ПРОМОКОД === #
    promo_waiting_code = State() # пользователь вводит промокод для активации

    # === ОБЫЧНОЕ ОБЩЕНИЕ === #
    # (пока не нужны, но можно добавить позже)
    # conversation = State()
