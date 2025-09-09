from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- НАСТРОЙКИ ---
ADMIN_ID = 6115656446  # 6115656446
CONTACTS_FILE = "contacts.txt"  # файл, где будем хранить контакты

# --- Функция для сохранения контакта в файл ---
def save_contact(info: str):
    with open(CONTACTS_FILE, "a", encoding="utf-8") as f:
        f.write(info + "\n")

# --- Функция для чтения контактов из файла ---
def read_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

# --- Команда /start ---
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Добро пожаловать!\n\n"
        "Если устал от «слива бюджета» и сложных схем — тут ты найдёшь простые и рабочие решения для рекламы в финансах.\n"
        "Поехали разбираться!"
    )
    keyboard = [[KeyboardButton("Поехали 🚀")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# --- Обработка кнопки "Поехали 🚀" ---
async def handle_go(update, context: ContextTypes.DEFAULT_TYPE):
    go_text = (
        "Понял тебя 👍\n\n"
        "🔥 Смотри, как это работает в двух словах:\n"
        "1⃣ Компаниям всегда нужны клиенты = деньги.\n"
        "2⃣ Они идут на партнёрские площадки, где выкладывают свой продукт.\n"
        "3⃣ За каждого приведённого клиента готовы платить от 300 ₽ до 20 000 ₽.\n"
        "4⃣ Я — тот самый человек, кто приводит им клиентов через рекламу и получает за это выплаты.\n"
        "💴 Всё просто: трафик → клиенты → деньги.\n\n"
        "Хочешь, я покажу, как это устроено изнутри? 😉\n"
        "Оставь свой контакт — и получишь подробности первым делом. 🚀"
    )

    keyboard = [[KeyboardButton("📱 Оставить контакт", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(go_text, reply_markup=reply_markup)

# --- Обработка сообщений (контакты и текст) ---
async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "не указан"

    # Если пользователь нажал "Поехали 🚀"
    if update.message.text == "Поехали 🚀":
        return await handle_go(update, context)

    # Если контакт
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        info = f"📩 Новый контакт!\nНомер: {phone_number}\nНик: {username}"
    else:
        user_input = update.message.text
        info = f"📩 Новый контакт!\nСообщение: {user_input}\nTelegram: {username}"

    # Сохраняем в файл
    save_contact(info)

    # Отправляем админу
    await context.bot.send_message(chat_id=ADMIN_ID, text=info)

    # Подтверждаем пользователю
    await update.message.reply_text("✅ Спасибо! Ваши данные получены.", reply_markup=ReplyKeyboardRemove())

# --- Команда /list (отправка последнего файла) ---
async def list_contacts(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        return await update.message.reply_text("⛔ У вас нет доступа к этому списку.")

    if not os.path.exists(CONTACTS_FILE):
        return await update.message.reply_text("📂 Список контактов пуст.")

    # Отправляем файл администратору
    await update.message.reply_document(document=InputFile(CONTACTS_FILE), filename=CONTACTS_FILE)

# --- Основной запуск ---
if __name__ == "__main__":
    app = ApplicationBuilder().token("8279924074:AAHZ4whiHOHwCZPnGOewVym9a8KGLYXZkIg").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_contacts))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Бот запущен...")
    app.run_polling()