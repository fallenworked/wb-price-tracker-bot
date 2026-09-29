import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, CHECK_INTERVAL_MINUTES
from db.database import Database
from bot.handlers import router
from services.scheduler import check_prices_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main():
    db = Database()
    await db.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Инициализация планировщика задач
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_prices_task, "interval", minutes=CHECK_INTERVAL_MINUTES, args=[bot, db])
    scheduler.start()

    logging.info("🚀 Бот-трекер цен Wildberries запущен!")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
