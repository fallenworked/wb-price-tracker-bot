import logging
from aiogram import Bot
from db.database import Database
from services.wb_parser import WBParser

async def check_prices_task(bot: Bot, db: Database):
    """Фоновая задача: проверяет новые цены для всех отслеживаемых товаров"""
    logging.info("🔄 Запуск фонового мониторинга цен WB...")
    articles = await db.get_all_unique_articles()

    for article in articles:
        info = await WBParser.get_product_info(article)
        if not info or info['price'] <= 0:
            continue

        new_price = info['price']
        subscribers = await db.get_subscribers_for_article(article)

        for sub in subscribers:
            old_price = sub['last_price']
            user_id = sub['user_id']
            title = sub['title']

            if new_price < old_price:
                diff = old_price - new_price
                percent = round((diff / old_price) * 100, 1)
                text = (
                    f"📉 <b>ЦЕНА УПАЛА!</b>\n\n"
                    f"📦 <b>{title}</b>\n"
                    f"💵 Старая цена: <s>{old_price} ₽</s>\n"
                    f"🔥 Новая цена: <b>{new_price} ₽</b> (Скидка {diff} ₽ / -{percent}%)\n\n"
                    f"🔗 <a href='https://www.wildberries.ru/catalog/{article}/detail.aspx'>Открыть на Wildberries</a>"
                )
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
                except Exception as e:
                    logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        # Обновляем последнюю цену и историю
        await db.update_price_and_history(article, new_price)
