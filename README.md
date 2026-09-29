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

## 🚀 Быстрый запуск

1. Клонировать репозиторий:
```bash
git clone [https://github.com/fallenworked/wb-price-tracker-bot.git](https://github.com/fallenworked/wb-price-tracker-bot.git)
cd wb-price-tracker-bot
