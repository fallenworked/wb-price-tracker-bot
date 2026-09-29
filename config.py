import os

# Telegram Bot Token от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "7777777777:YOUR_TELEGRAM_BOT_TOKEN_HERE")

# Интервал проверки цен в минутах (по умолчанию каждые 30 минут)
CHECK_INTERVAL_MINUTES = 30

# Путь к базе данных
DB_NAME = "tracker.db"
