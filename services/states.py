from aiogram.fsm.state import State, StatesGroup


class StateMachine(StatesGroup):
    """Машина состояний для бота"""

    # === АДМИН ПАНЕЛЬ === #
    admin_main_menu = State()
    admin_waiting_user_id_for_info = State()
    admin_waiting_user_id_for_options = State()
    admin_waiting_options_data = State()

    # === ОБЫЧНОЕ ОБЩЕНИЕ === #
    # (пока не нужны, но можно добавить позже)
    # conversation = State()
