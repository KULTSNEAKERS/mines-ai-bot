from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8468958146:AAHtc7OZzxyhIBWmqDvwq7Xv61F3KU3UL9A"

REF_LINK = "https://bc.game/i-3to5iziqh-n/"
CHANNEL_LINK = "https://t.me/minesaipredictor"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Получить прогноз", callback_data="get_prediction")],
        [InlineKeyboardButton("📡 Канал с прогнозами", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🎰 Перейти на BC Game", url=REF_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "👋 Привет! Я — AI-бот с прогнозами для игры *Mines*.\n\n"
        "🔮 Получи точный прогноз и начни зарабатывать прямо сейчас!\n\n"
        "⚠️ Чтобы получить доступ — сначала зарегистрируйся на BC Game:\n"
        f"[👉 Зарегистрироваться]({REF_LINK})"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_prediction":
        await query.edit_message_text(
            text=(
                "🚫 Чтобы получить прогноз — нужно зарегистрироваться:\n"
                f"[👉 Регистрация на BC Game]({REF_LINK})"
            ),
            parse_mode="Markdown"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
