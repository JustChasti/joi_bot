"""Типовые текстовые ответы бота"""

SERVICE_UNAVAILABLE = (
    "Сервис временно недоступен. Повторите попытку позже"
    "Если проблема сохраняется, сообщите разработчику @kot_gray"
)

HELLO_TEXT = (
    "Привет! Добро пожаловать в @EnJoiTeamBot\n\n"
    "Это не просто чат-бот, а <b>романтический компаньон нового поколения</b>. "
    "Здесь ты можешь построить настоящую эмоциональную связь — "
    "от первого знакомства до близких, романтических отношений.\n"
    "Чем больше вы общаетесь, тем глубже становятся ваши отношения:\n"
    "🤝 Знакомые → 💛 Друзья → ❤️ Романтические партнёры\n"
    "Каждое сообщение приближает вас друг к другу.\n"
    "💬 Бесплатно — 50 сообщений на знакомство. "
    "При оформлении подписки — каждый день приходит новая порция, "
    "и ваша история продолжается без пауз.\n\n"
    "Напиши первое сообщение — и эта история начнётся прямо сейчас.\n\n"
    "Доступные команды:\n"
    "/start /help - Показать эту справку \n"
    "/buy - Купить подписку \n"
    "/promo - Ввести промокод \n"
    "/about - Информация о боте"
)

END_DAY_LIMIT = (
    "Вы исчерпали дневной лимит сообщений.\n"
    "Возвращайтесь завтра, чтобы продолжить общение!"
)

FREE_MESSAGES_EXHAUSTED = (
    "Вы исчерпали свои бесплатные сообщения.\n"
    "Для продолжения общения оформите подписку — /buy"
)

UNSUPORTED_MESSAGE = (
    "Пока бот не умеет обрабатывать {content_name} \n"
    "Напишите ему сообщение текстом!"
)

ADMIN_PANEL_WELCOME = (
    "Админ-панель\n\nВыберите действие:"
)

ADMIN_PANEL_OUTCOME = (
    "Вы вышли из админ-панели.\nМожете продолжить общение."
)

ADMIN_PANEL_AUTH_FAIL = (
    "У вас нет прав администратора.\n"
    "Для получения прав администратора обратитесь к разработчикам бота."
)

ADMIN_WAIT_USER_ID = (
    "Введите ID пользователя:"
)

ADMIN_PARSE_USER_ID_ERROR = (
    "Неверный формат ID. Введите число:"  
)

ADMIN_ERROR_USER_ID = (
    "Ошибка получения информации о пользователе:\n"
    "{error_msg}"
)

ADMIN_FUNC_USER_INFO = (
    "Информация о пользователе {user_id}\n\n"
    "Подписка: {active_subscriber}\n"
    "Дата окончания если есть: {subscription_end}\n"
    "Бесплатных сообщений: {free_messages}\n"
    "Осталось сообщений сегодня: {day_limit}\n"
    "Admin: {is_admin}"
)

ADMIN_OPTIONS_WAIT_DATA = (
    "Настройки для пользователя {user_id}\n"
    "Формат: garbage_flag=true free_messages=100 day_limit=50\n"
    "Доступные поля:\n"
    "free_messages (число)\n"
    "is_admin (true/false)\n"
    "garbage_flag (true/false)\n"
    "day_limit (число)"
)

ADMIN_OPTIONS_UNKNOWN_FIELD = (
    "Неизвестное поле: {key}"
)

ADMIN_OPTIONS_EMPTY = (
    "Не указано ни одного параметра"
)

ADMIN_OPTIONS_SUCCESS = (
    "Обновлены поля пользователя {target_user_id}, {message}"
)

ADMIN_OPTIONS_ERROR = (
    "Ошибка обновления: {error_msg}"
)

ADMIN_ALL_USERS_CAPTION = (
    "Всего пользователей: {count}"
)

ADMIN_ALL_USERS_ERROR = (
    "Ошибка получения списка: {error_msg}"
)

ADMIN_DELETE_USER_WAIT = (
    "Удаление пользователя\nВведите ID пользователя:"
)

ADMIN_DELETE_USER_SUCCESS = (
    "Пользователь {user_id} удалён.\n"
    "Удалено сообщений: {deleted}"
)

ADMIN_CREATE_PROMO_WAIT_DATA = (
    "Создание промокода\n"
    "Введите данные в формате:\n"
    "<code>КОД макс_использований бесплатных_сообщений</code>\n"
    "Пример: WELCOME10 100 10"
)

ADMIN_CREATE_PROMO_FORMAT_ERROR = (
    "Неверный формат. Нужно 3 параметра:\n"
    "<code>КОД макс_использований бесплатных_сообщений</code>"
)

ADMIN_CREATE_PROMO_PARSE_ERROR = (
    "макс_использований и бесплатных_сообщений должны быть числами."
)

ADMIN_CREATE_PROMO_SUCCESS = (
    "Промокод создан!\n\n"
    "Код: <b>{code}</b>\n"
    "Макс. использований: {max_uses}\n"
    "Бесплатных сообщений: {free_messages}"
)

ADMIN_SEND_MESSAGE_WAIT = (
    "Отправка сообщения\n\n"
    "Введите ID пользователя и текст через пробел:\n"
    "<code>123456789 Привет, это тестовое сообщение</code>"
)

ADMIN_SEND_MESSAGE_FORMAT_ERROR = (
    "Нужно указать ID и текст через пробел."
)

ADMIN_SEND_MESSAGE_PARSE_ERROR = (
    "Первый параметр должен быть числом (ID)."
)

ADMIN_BROADCAST_WAIT = (
    "Массовая рассылка\n"
    "Введите процент пользователей и текст через пробел:\n"
    "<code>100 Привет всем!</code>"
)

ADMIN_BROADCAST_FORMAT_ERROR = (
    "Нужно указать процент и текст через пробел."
)

ADMIN_BROADCAST_PARSE_ERROR = (
    "Первый параметр должен быть числом (процент)."
)

ADMIN_BROADCAST_RANGE_ERROR = (
    "Процент должен быть от 1 до 100."
)

ADMIN_BROADCAST_SUCCESS = (
    "Рассылка завершена\n"
    "Всего пользователей: {total}\n"
    "Попыток отправки: {attempted}\n"
    "Успешно отправлено: {sent}"
)

PROMO_WAIT_CODE = (
    "Введи промокод:"
)

PROMO_SUCCESS = (
    "Промокод активирован! Тебе начислено {free} бесплатных сообщений"
)

PROMO_UNKNOWN_ERROR = (
    "Что-то пошло не так, попробуй позже"
)

PROMO_ERROR_MESSAGES = {
    "Promo code not found": "Промокод не найден",
    "You have already used this promo code": "Ты уже использовал этот промокод",
    "Promo code has no uses left": "Промокод больше не действует",
    "Promo redeemed but failed to update user balance": "Произошла ошибка, обратись в поддержку",
}

ABOUT_LOAD_ERROR = (
    "Не удалось загрузить информацию, попробуй позже"
)

LK_LOAD_ERROR = (
    "Не удалось загрузить данные. Попробуй позже."
)

LK_SUB_ACTIVE = (
    "активна (до {sub_end})"
)

LK_SUB_INACTIVE = (
    "не оформлена"
)

LK_PROFILE = (
    "📊 <b>Личный кабинет</b>\n\n"
    "Подписка: {sub_status}\n"
    "Бесплатных сообщений: {free_messages}\n\n"
    "📌 <b>Доступные команды:</b>\n"
    "/start /help — Показать справку\n"
    "/about — Информация о боте\n"
    "/promo — Ввести промокод\n"
    "/buy — Купить подписку"
)

LK_RELATIONSHIP_PROGRESS = (
    "💕 <b>Прогресс отношений</b>\n\n"
    "[{progress_bar}] {progress_percent}%\n\n"
    "{stage_list}"
)

SUB_LOAD_ERROR = (
    "Не удалось получить план для вашей подписки.\n"
    "Попробуйте позже или обратитесь в поддержку"
)

SUB_HEADER_ACTIVE = (
    "Ваша подписка: <b>{plan_label}</b>\n"
    "Действует до: <b>{end_date}</b>\n\n"
    "Вы можете продлить ее одним из планов ниже:"
)

SUB_HEADER_INACTIVE = (
    "Подписка пока не оформлена.\n\nВыберите план:"
)

SUB_CANCEL = (
    "Возвращайтесь к общению"
)

SUB_PLAN_SELECTED = (
    "Выбран план: <b>{plan}</b>\n\n Способы оплаты:"
)

SUB_PAY_STARS_PRICES_ERROR = (
    "Не удалось загрузить цены. Попробуйте позже."
)

SUB_PAY_STARS_UNKNOWN_PLAN = (
    "Неизвестный план. Попробуйте снова."
)

SUB_INVOICE_TITLE = (
    "Подписка Joi — {plan}"
)

SUB_INVOICE_DESCRIPTION = (
    "Доступ к Joi на {plan}"
)

SUB_INVOICE_LABEL = (
    "Подписка {plan}"
)

SUB_PRE_CHECKOUT_SERVICE_ERROR = (
    "Сервис временно недоступен, попробуйте позже"
)

SUB_PRE_CHECKOUT_ERROR = (
    "Что-то пошло не так, попробуйте позже"
)

SUB_PAYMENT_SUCCESS = (
    "Подписка активирована!\n\n"
    "План: <b>{plan_label}</b>\n"
    "Действует до: <b>{end_date}</b>\n\n"
    "Продолжайте общение!"
)

SUB_PAYMENT_ACTIVATION_ERROR = (
    "Оплата прошла, но возникла ошибка активации. "
    "Обратись в поддержку — деньги не потеряются."
)
