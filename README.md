# 🤖 Joi Bot - Telegram Bot с AI интеграцией

Telegram бот на базе aiogram для взаимодействия с AI-ассистентом "Джой". Бот принимает сообщения пользователей, отправляет их на backend API и возвращает ответы в Telegram.

## 📋 Возможности

- ✅ Обработка команд `/start` и `/help`
- ✅ Отправка сообщений пользователей на API сервер
- ✅ Асинхронная обработка запросов
- ✅ Обработка ошибок с логированием
- ✅ Конфигурация через переменные окружения
- ✅ Настраиваемые текстовые приветствия

## 🛠 Технологии

- **Python 3.12+**
- **aiogram 3.22.0** - фреймворк для Telegram ботов
- **aiohttp 3.12.15** - асинхронные HTTP запросы
- **loguru 0.7.3** - логирование
- **python-dotenv** - управление переменными окружения

## 📁 Структура проекта

```
joi_bot/
├── config/                    # Конфигурация
│   ├── config.py             # Настройки приложения
│   └── texts/                # Текстовые файлы
│       └── hello.txt         # Приветственное сообщение
├── services/                 # Бизнес-логика
│   ├── api_requests.py       # API клиент
│   ├── decorators.py         # Декораторы обработки ошибок
│   ├── handlers.py           # Обработчики команд
│   └── resolver.py           # Логика обработки сообщений
├── .env                      # Переменные окружения (не в git!)
├── .gitignore               # Игнорируемые файлы
├── main.py                  # Точка входа
├── requirements.txt         # Зависимости
└── README.md               # Документация
```

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/JustChasti/joi_bot.git
cd joi_bot
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Токен бота от BotFather
BOT_TOKEN=your_bot_token_here

# Настройки сервера
SERVER_HOST=http://127.0.0.1:8080
API_PATH=/api/v1
```

### 5. Получение токена бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

### 6. Запуск бота

```bash
python main.py
```

При успешном запуске вы увидите:
```
2025-10-02 12:00:00 | INFO | Запуск бота...
2025-10-02 12:00:00 | INFO | Конфигурация загружена. Server URL: http://127.0.0.1:8080
2025-10-02 12:00:00 | INFO | Бот запущен!
```

## 📡 API интеграция

Бот отправляет POST запросы на сервер по адресу: `{SERVER_HOST}{API_PATH}/message`

**Формат запроса:**
```json
{
  "user_id": "123456789",
  "content": "текст сообщения пользователя"
}
```

**Ожидаемый формат ответа:**
```json
{
  "response": "ответ от AI модели",
  "status": "success"
}
```

## 🎮 Использование

### Команды бота

- `/start` - Начать общение с ботом, показать приветствие
- `/help` - Показать справку

### Общение

Просто отправьте любое текстовое сообщение боту, и он перешлёт его на AI сервер, затем вернёт ответ.

## ⚙️ Конфигурация

### Изменение приветственного сообщения

Отредактируйте файл `config/texts/hello.txt`:

```text
Знакомься, Это Джой!
Не просто ИИ ассистент, а настоящая девушка
...
```

### Переменные окружения

| Переменная | Описание | По умолчанию |
|-----------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота | (обязательно) |
| `SERVER_HOST` | Адрес API сервера | `http://127.0.0.1:8080` |
| `API_PATH` | Базовый путь API | `/api/v1` |

## 🔧 Разработка

### Обработка ошибок

Проект использует декораторы для обработки ошибок:

```python
from services.decorators import handle_errors_async

@handle_errors_async
async def my_function():
    # Ваш код
    pass
```

Доступные декораторы:
- `handle_errors` - для обычных функций
- `handle_errors_method` - для методов класса
- `handle_errors_async` - для асинхронных функций
- `handle_errors_async_method` - для асинхронных методов класса

### Логирование

Проект использует `loguru` для логирования:

```python
from loguru import logger

logger.info("Информационное сообщение")
logger.error("Ошибка", exc_info=True)
```

### Добавление новых команд

1. Откройте `services/handlers.py`
2. Добавьте новый обработчик:

```python
@router.message(Command("new_command"))
async def cmd_new(message: Message):
    await message.answer("Ответ на новую команду")
```

## 🐛 Отладка

### Проверка подключения к API

```bash
curl -X POST http://127.0.0.1:8080/api/v1/message \
  -H "Content-Type: application/json" \
  -d '{"user_id":"123","content":"test"}'
```

### Логи

Все логи выводятся в консоль. Уровень логирования можно настроить в коде.

## 📝 TODO

- [ ] Добавить кэширование текстовых файлов
- [ ] Реализовать пул соединений для API клиента
- [ ] Добавить rate limiting
- [ ] Добавить базу данных для хранения истории
- [ ] Добавить inline кнопки
- [ ] Добавить обработку медиа-файлов
- [ ] Добавить тесты

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'feat: add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект создан для образовательных целей.

## 👤 Автор

**JustChasti**

- GitHub: [@JustChasti](https://github.com/JustChasti)
- Telegram: [Свяжитесь со мной](https://t.me/your_username)

## 🙏 Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - отличный фреймворк для Telegram ботов
- [Telegram Bot API](https://core.telegram.org/bots/api) - за предоставление API

---

⭐ Если проект был полезен, поставьте звёздочку на GitHub!