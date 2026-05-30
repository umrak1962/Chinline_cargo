import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes
)

BOT_TOKEN = "8396886635:AAECKFSL7oa-j9-N5S1ZbKLSkFzoqaxP-Vk"
ADMIN_ID  = 7506336374

logging.basicConfig(level=logging.INFO)

FROM_CITY, TO_CITY, GOODS_TYPE, PHOTO, DIMENSIONS, WEIGHT, PACKAGING, QUANTITY, PRICE, CONTACT, CONFIRM = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🚚 Xitoy Kargo Xizmatiga Xush Kelibsiz!\n"
        "Добро пожаловать в Китайское Карго!\n\n"
        "Buyurtma berish uchun quyidagi tugmani bosing.\n"
        "Для оформления заказа нажмите кнопку ниже. 👇",
        reply_markup=ReplyKeyboardMarkup([["📦 Buyurtma berish / Оформить заказ"]], resize_keyboard=True)
    )
    return FROM_CITY

async def ask_from_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1️⃣ Yuk qayerdan olinadi? (Xitoyda shahar)\n"
        "Откуда забрать груз? (Город в Китае)\n\n"
        "Misol: Guangzhou, Yiwu, Shanghai",
        reply_markup=ReplyKeyboardRemove()
    )
    return FROM_CITY

async def get_from_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['from_city'] = update.message.text
    await update.message.reply_text(
        "2️⃣ Yuk qayerga yetkazilsin? (O'zbekistonda shahar)\n"
        "Куда доставить? (Город в Узбекистане)\n\n"
        "Misol: Toshkent, Samarqand, Andijon"
    )
    return TO_CITY

async def get_to_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['to_city'] = update.message.text
    await update.message.reply_text(
        "3️⃣ Qanday tovar?\n"
        "Что за товар?\n\n"
        "Misol: Kiyim, elektronika, mebel, oziq-ovqat..."
    )
    return GOODS_TYPE

async def get_goods_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['goods_type'] = update.message.text
    await update.message.reply_text(
        "4️⃣ Tovar rasmini yuboring 📸\n"
        "Пришлите фото товара 📸\n\n"
        "Rasm yo'q bo'lsa yozing: Rasm yo'q\n"
        "Нет фото — напишите: Нет фото"
    )
    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data['photo_id'] = update.message.photo[-1].file_id
        context.user_data['has_photo'] = True
    else:
        context.user_data['has_photo'] = False
    await update.message.reply_text(
        "5️⃣ O'lchamlari (uzunlik × kenglik × balandlik, sm)\n"
        "Размеры (длина × ширина × высота, см)\n\n"
        "Misol: 50×30×20"
    )
    return DIMENSIONS

async def get_dimensions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['dimensions'] = update.message.text
    await update.message.reply_text(
        "6️⃣ Umumiy og'irlik (kg)\n"
        "Общий вес (кг)\n\n"
        "Misol: 100 kg"
    )
    return WEIGHT

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['weight'] = update.message.text
    await update.message.reply_text(
        "7️⃣ Qadoqlash turi\n"
        "Вид упаковки\n\n"
        "Misol: Quti, Qop, Plyonka, Yog'och qafas"
    )
    return PACKAGING

async def get_packaging(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['packaging'] = update.message.text
    await update.message.reply_text(
        "8️⃣ Nechta joy (dona/quti/qop soni)\n"
        "Количество мест\n\n"
        "Misol: 10 quti"
    )
    return QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['quantity'] = update.message.text
    await update.message.reply_text(
        "9️⃣ Tovar taxminiy qiymati ($)\n"
        "Примерная стоимость товара ($)\n\n"
        "Misol: $500"
    )
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text(
        "🔟 Telefon raqamingiz\n"
        "Ваш номер телефона\n\n"
        "Misol: +998 90 123 45 67"
    )
    return CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact'] = update.message.text
    d = context.user_data
    summary = (
        f"✅ Ma'lumotlarni tekshiring / Проверьте данные:\n\n"
        f"📍 Qayerdan / Откуда: {d.get('from_city')}\n"
        f"📍 Qayerga / Куда: {d.get('to_city')}\n"
        f"📦 Tovar / Товар: {d.get('goods_type')}\n"
        f"📐 O'lcham / Размер: {d.get('dimensions')}\n"
        f"⚖️ Og'irlik / Вес: {d.get('weight')}\n"
        f"🎁 Qadoq / Упаковка: {d.get('packaging')}\n"
        f"🔢 Miqdor / Кол-во: {d.get('quantity')}\n"
        f"💵 Qiymat / Стоимость: {d.get('price')}\n"
        f"📞 Telefon / Телефон: {d.get('contact')}\n\n"
        f"To'g'rimi? / Всё верно?"
    )
    await update.message.reply_text(
        summary,
        reply_markup=ReplyKeyboardMarkup(
            [["✅ Ha, yuborish / Отправить", "❌ Qayta / Заново"]],
            resize_keyboard=True
        )
    )
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "Qayta" in update.message.text or "Заново" in update.message.text:
        return await start(update, context)

    d = context.user_data
    user = update.effective_user

    admin_msg = (
        f"🆕 YANGI BUYURTMA / НОВЫЙ ЗАКАЗ\n"
        f"{'='*35}\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"🔗 Username: @{user.username or 'yoq'}\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"{'='*35}\n"
        f"📍 Qayerdan: {d.get('from_city')}\n"
        f"📍 Qayerga: {d.get('to_city')}\n"
        f"📦 Tovar: {d.get('goods_type')}\n"
        f"📐 O'lcham: {d.get('dimensions')}\n"
        f"⚖️ Og'irlik: {d.get('weight')}\n"
        f"🎁 Qadoq: {d.get('packaging')}\n"
        f"🔢 Miqdor: {d.get('quantity')}\n"
        f"💵 Qiymat: {d.get('price')}\n"
        f"📞 Telefon: {d.get('contact')}\n"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)

    if d.get('has_photo') and d.get('photo_id'):
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=d['photo_id'],
            caption=f"📸 Tovar rasmi — {d.get('goods_type')} ({user.full_name})"
        )

    await update.message.reply_text(
        "✅ Buyurtmangiz qabul qilindi! Tez orada bog'lanamiz.\n"
        "✅ Заказ принят! Скоро свяжемся с вами. 🚀",
        reply_markup=ReplyKeyboardMarkup([["📦 Yangi buyurtma / Новый заказ"]], resize_keyboard=True)
    )
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi. /start", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("Buyurtma|Оформить|Yangi|Новый"), ask_from_city)
        ],
        states={
            FROM_CITY:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_from_city)],
            TO_CITY:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_to_city)],
            GOODS_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goods_type)],
            PHOTO:      [MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), get_photo)],
            DIMENSIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dimensions)],
            WEIGHT:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            PACKAGING:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_packaging)],
            QUANTITY:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            PRICE:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            CONTACT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            CONFIRM:    [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("✅ Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
