# 📦 Wildberries Price Tracker & Analytics Telegram Bot

Современный асинхронный Telegram-бот на **aiogram 3** для мониторинга цен на маркетплейсе **Wildberries** с графиками аналитики и фоновыми уведомлениями.

## ⚡ Функционал
- 🔍 **Автоматический разбор ссылок и артикулов WB**.
- 📉 **Мониторинг цен в фоновом режиме** (кастомизируемый интервал проверки).
- 📊 **Генерация графиков истории цен** в виде изображений (`matplotlib`).
- 🔔 **Мгновенные Telegram-уведомления** при падении цены.
- 🗄 **Асинхронная БД SQLite** (`aiosqlite`) с сохранением истории изменений.

## 🛠️ Стек технологий
- **Python 3.10+**
- **aiogram 3.x** (Telegram Bot API Framework)
- **httpx** (Асинхронные HTTP-запросы)
- **APScheduler** (Фоновые периодические задачи)
- **Matplotlib & Pillow** (Визуализация данных и графики)
- **aiosqlite** (Async SQLite driver)

## 📁 Структура проекта
```text
wb-price-tracker-bot/
├── bot/
│   ├── __init__.py
│   ├── handlers.py        # Обработчики команд и сообщений
│   └── keyboards.py       # Инлайн-клавиатуры
├── db/
│   ├── __init__.py
│   └── database.py        # Асинхронная работа с БД SQLite
├── services/
│   ├── __init__.py
│   ├── wb_parser.py       # Парсер API Wildberries
│   ├── chart.py           # Генерация графиков цен
│   └── scheduler.py       # Фоновая проверка цен
├── config.py              # Конфигурация и переменные
├── main.py                # Точка входа
├── requirements.txt
└── README.md
```

## 🚀 Быстрый запуск

1. Клонировать репозиторий:
```bash
git clone [https://github.com/fallenworked/wb-price-tracker-bot.git](https://github.com/fallenworked/wb-price-tracker-bot.git)
cd wb-price-tracker-bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Указать `BOT_TOKEN` в `config.py` (получить у [@BotFather](https://t.me/BotFather)).

4. Запустить бота:
```bash
python main.py
```

## 👨‍💻 Автор и контакты
- **Автор**: fallenworked
- **GitHub**: [fallenworked](https://github.com/fallenworked)
- **Telegram**: [@caxaold](https://t.me/caxaold)
