from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import random

# 🔐 Твои данные
TOKEN = '8468958146:AAHtc7OZzxyhIBWmqDvwq7Xv61F3KU3UL9A'
REF_LINK = 'https://bc.game/i-3to5iziqh-n/'
CHANNEL_LINK = 'https://t.me/minesaipredictor'

# Фейковые клетки и стратегии
cells = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5",
         "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5",
         "E1", "E2", "E3", "E4", "E5"]
strategies = ["Ромб", "Змейка", "Лестница", "Диагональ", "Сектор", "Рандом волна"]

# Ограничение — храним ID пользователей, кто уже получил прогноз
predicted_users = set()

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🎯 Получить прогноз", callback_data='predict')],
        [InlineKeyboardButton("🎰 Перейти в казино", url=REF_LINK)],
        [InlineKeyboardButton("📢 Наш канал", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "🤖 Добро пожаловать в *AI Mines Predictor Bot*!\n\n"
        "Я анализирую игровые поля MINES на основе алгоритмов и паттернов поведения игроков.\n\n"
        "🎯 *Точность предсказаний*: до 90%\n"
        "🧠 *Алгоритмы*: ромб, змейка, лестница, спираль\n"
        f"📢 *Канал с обновлениями*: [@minesaipredictor]({CHANNEL_LINK})\n"
        f"🎰 *Играйте с ИИ*: [BC.Game по ссылке]({REF_LINK})\n\n"
        "👇 Выберите действие:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def predict_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    # Если пользователь уже получал прогноз
    if user_id in predicted_users:
        keyboard = [
            [InlineKeyboardButton("🎰 Зарегистрироваться", url=REF_LINK)],
            [InlineKeyboardButton("🔙 Назад", callback_data='back')]
        ]
        query.edit_message_text(
            text=(
                "⚠️ Чтобы получить следующий прогноз, необходимо зарегистрироваться на BC.Game по ссылке ниже.\n\n"
                f"🔗 {REF_LINK}"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Первый прогноз — разрешаем
    predicted_users.add(user_id)
    prediction = random.sample(cells, 3)
    strategy = random.choice(strategies)
    accuracy = random.randint(84, 97)

    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='back')],
        [InlineKeyboardButton("🎰 Перейти в казино", url=REF_LINK)]
    ]

    query.edit_message_text(
        text=(
            f"🧠 *ИИ предсказание готово!*\n"
            f"✅ *Безопасные клетки*: {', '.join(prediction)}\n"
            f"📈 *Точность*: {accuracy}%\n"
            f"🎯 *Алгоритм*: {strategy}\n\n"
            f"👉 Играй: {REF_LINK}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def back_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🎯 Получить прогноз", callback_data='predict')],
        [InlineKeyboardButton("🎰 Перейти в казино", url=REF_LINK)],
        [InlineKeyboardButton("📢 Наш канал", url=CHANNEL_LINK)]
    ]
    query.edit_message_text(
        text=(
            "🤖 Добро пожаловать в *AI Mines Predictor Bot*!\n\n"
            "Я анализирую игровые поля MINES на основе алгоритмов и паттернов поведения игроков.\n\n"
            "🎯 *Точность предсказаний*: до 90%\n"
            "🧠 *Алгоритмы*: ромб, змейка, лестница, спираль\n"
            f"📢 *Канал с обновлениями*: [@minesaipredictor]({CHANNEL_LINK})\n"
            f"🎰 *Играйте с ИИ*: [BC.Game по ссылке]({REF_LINK})\n\n"
            "👇 Выберите действие:"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(predict_callback, pattern='^predict$'))
    dp.add_handler(CallbackQueryHandler(back_callback, pattern='^back$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
