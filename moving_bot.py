from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

(LOCATION_FROM, LOCATION_TO, ROOMS, ELEVATOR, SERVICES) = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу рассчитать стоимость переезда. Откуда выезжаешь?")
    return LOCATION_FROM

async def location_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location_from'] = update.message.text
    await update.message.reply_text("Куда переезжаешь?")
    return LOCATION_TO

async def location_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location_to'] = update.message.text
    await update.message.reply_text("Сколько комнат?")
    return ROOMS

async def rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rooms'] = update.message.text
    reply_keyboard = [["Да", "Нет"]]
    await update.message.reply_text("Есть ли лифт?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ELEVATOR

async def elevator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['elevator'] = update.message.text
    await update.message.reply_text("Нужны ли доп. услуги (упаковка, разборка мебели и т.д.)?")
    return SERVICES

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['services'] = update.message.text
    base_price = 300
    try:
        base_price += int(context.user_data['rooms']) * 100
    except:
        pass
    if context.user_data['elevator'].lower() == "нет":
        base_price += 50
    if "упаковка" in context.user_data['services'].lower():
        base_price += 100

    text = (
        f"📦 Переезд из: {context.user_data['location_from']}\n"
"
        f"📍 В: {context.user_data['location_to']}
"
        f"🏠 Комнат: {context.user_data['rooms']}
"
        f"🛗 Лифт: {context.user_data['elevator']}
"
        f"🧰 Услуги: {context.user_data['services']}

"
        f"💵 Предварительная цена: ${base_price}"
    )
    await update.message.reply_text(text)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, если передумаешь — напиши /start.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("8046912572:AAHT44deUUK7Hael7QuHuZJszwkKrn16sOE").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOCATION_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_from)],
            LOCATION_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_to)],
            ROOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, rooms)],
            ELEVATOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, elevator)],
            SERVICES: [MessageHandler(filters.TEXT & ~filters.COMMAND, services)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
