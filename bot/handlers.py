from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart
from services.wb_parser import WBParser
from services.chart import generate_price_chart
from bot.keyboards import main_keyboard, item_control_keyboard
from db.database import Database

router = Router()
db = Database()

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 **Привет! Я бот-трекер цен Wildberries.**\n\n"
        "Пришли мне **артикул** или **ссылку на товар**, и я буду отслеживать его цену.\n"
        "Как только цена снизится — я сразу пришлю тебе уведомление! 🚀"
    )
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "my_items")
async def process_my_items(callback: CallbackQuery):
    items = await db.get_user_trackings(callback.from_user.id)
    if not items:
        await callback.message.edit_text("📭 У вас пока нет отслеживаемых товаров.\nОтправьте артикул товара!", reply_markup=main_keyboard())
        return

    text = "📋 **Ваши отслеживаемые товары:**\n\n"
    for idx, item in enumerate(items, 1):
        text += f"{idx}. **{item['title']}**\n• Артикул: `{item['article']}` | Цена: **{item['last_price']} ₽**\n\n"

    # Для простоты предлагаем ввести артикул для деталей
    text += "Нажмите на кнопку с артикулом ниже для просмотра деталей и графика:"
    
    keyboard_buttons = []
    for item in items:
        keyboard_buttons.append([InlineKeyboardButton(text=f"📦 {item['article']} - {item['last_price']}₽", callback_data=f"view_{item['article']}")])
    keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Главное меню", callback_data="help")])

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons), parse_mode="Markdown")

@router.callback_query(F.data.startswith("view_"))
async def process_view_item(callback: CallbackQuery):
    article = int(callback.data.split("_")[1])
    items = await db.get_user_trackings(callback.from_user.id)
    item = next((i for i in items if i['article'] == article), None)

    if not item:
        await callback.answer("Товар не найден!")
        return

    text = (
        f"📦 **{item['title']}**\n\n"
        f"• Артикул: `{item['article']}`\n"
        f"• Текущая цена: **{item['last_price']} ₽**\n"
        f"• Ссылка: [Открыть WB](https://www.wildberries.ru/catalog/{article}/detail.aspx)"
    )
    await callback.message.edit_text(text, reply_markup=item_control_keyboard(article), parse_mode="Markdown", disable_web_page_preview=True)

@router.callback_query(F.data.startswith("chart_"))
async def process_chart(callback: CallbackQuery):
    article = int(callback.data.split("_")[1])
    items = await db.get_user_trackings(callback.from_user.id)
    item = next((i for i in items if i['article'] == article), None)

    history = await db.get_price_history(article)
    if not history or len(history) < 1:
        await callback.answer("История цен пока пуста. Зайдите позже!")
        return

    await callback.answer("Генерирую график...")
    chart_buf = generate_price_chart(article, item['title'] if item else str(article), history)
    
    photo = BufferedInputFile(chart_buf.read(), filename=f"chart_{article}.png")
    await callback.message.answer_photo(photo=photo, caption=f"📊 График изменения цены для артикула `{article}`", parse_mode="Markdown")

@router.callback_query(F.data.startswith("del_"))
async def process_delete(callback: CallbackQuery):
    article = int(callback.data.split("_")[1])
    await db.delete_tracking(callback.from_user.id, article)
    await callback.answer("✅ Товар удален из отслеживания!")
    await process_my_items(callback)

@router.message()
async def handle_article_input(message: Message):
    article = WBParser.extract_article(message.text)
    if not article:
        await message.answer("⚠️ Не удалось распознать артикул Wildberries. Отправьте ссылку или числовой артикул.")
        return

    msg = await message.answer("🔍 Ищу товар на Wildberries...")
    info = await WBParser.get_product_info(article)

    if not info:
        await msg.edit_text("❌ Товар не найден на Wildberries. Проверьте артикул.")
        return

    await db.add_tracking(message.from_user.id, info['article'], info['title'], info['price'])

    text = (
        f"✅ **Товар добавлен в отслеживание!**\n\n"
        f"📦 **{info['title']}**\n"
        f"🏷 Бренд: {info['brand']}\n"
        f"💵 Текущая цена: **{info['price']} ₽**\n\n"
        f"Я пришлю сообщение, как только цена снизится!"
    )
    await msg.edit_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")
