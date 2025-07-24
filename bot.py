from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from collections import defaultdict

TOKEN = "8468958146:AAHtc7OZzxyhIBWmqDvwq7Xv61F3KU3UL9A"
REF_LINK = "https://bc.game/i-3to5iziqh-n/"
CHANNEL_LINK = "https://t.me/minesaipredictor"
ADMIN_ID = 939790185  # твой Telegram ID

# Хранилище количества прогнозов
user_data = defaultdict(lambda: {"free": 3, "reg_bonus": 0, "registered": False})

# Главное меню
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Получить прогноз", callback_data="get_prediction")],
        [InlineKeyboardButton("📡 Канал с прогнозами", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🎰 Перейти на BC Game", url=REF_LINK)]
    ])

# Меню внутри "Получить прогноз"
def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=(
            "👋 Привет! Я — AI-бот с прогнозами для игры *Mines*.\n\n"
            "🔮 Получи точный прогноз и начни зарабатывать прямо сейчас!\n\n"
            "⚠️ Чтобы получить доступ — сначала зарегистрируйся:\n"
            f"[👉 Зарегистрироваться]({REF_LINK})"
        ),
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = user_data[user_id]

    # Получить прогноз
    if query.data == "get_prediction":
        # Админ — безлимит
        if user_id == ADMIN_ID:
            await query.edit_message_text("🎯 Прогноз: 💣 в клетке C3\n(Ты админ, ограничений нет)", reply_markup=back_menu())
            return

        if user["free"] > 0:
            user["free"] -= 1
            await query.edit_message_text(
                f"🎯 Прогноз: 💣 в клетке B2\n\n📦 Осталось бесплатных прогнозов: {user['free']}",
                reply_markup=back_menu()
            )
        elif not user["registered"]:
            await query.edit_message_text(
                "⚠️ Бесплатные прогнозы закончились.\n\n"
                f"👉 Зарегистрируйся на BC Game по ссылке, чтобы получить ещё 5 прогнозов:\n{REF_LINK}\n\n"
                "После регистрации — нажми кнопку ниже 👇",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Я зарегистрировался", callback_data="confirm_register")],
                    [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
                ])
            )
        elif user["reg_bonus"] > 0:
            user["reg_bonus"] -= 1
            await query.edit_message_text(
                f"🎯 Прогноз: 💣 в клетке A1\n\n📦 Осталось прогнозов после регистрации: {user['reg_bonus']}",
                reply_markup=back_menu()
            )
        else:
            await query.edit_message_text(
                "⚠️ Прогнозы закончились.\n\n🔄 Зарегистрируй новый аккаунт, чтобы получить ещё!",
                reply_markup=back_menu()
            )

    # Подтверждение регистрации
    elif query.data == "confirm_register":
        user["registered"] = True
        user["reg_bonus"] = 5
        await query.edit_message_text(
            "✅ Готово! Ты получил ещё 5 прогнозов.\n\nНажми кнопку ниже, чтобы продолжить:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 Получить прогноз", callback_data="get_prediction")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
            ])
        )

    # Назад в главное меню
    elif query.data == "back_to_main":
        await query.edit_message_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
