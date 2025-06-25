import telebot
from telebot import types

# Токен бота
BOT_TOKEN = '8090540025:AAHTwjbfXSUh0R8fcc83XfFypF1lA-M09Vw'  # замените на свой токен
bot = telebot.TeleBot(BOT_TOKEN)

# ID вашего канала
CHANNEL_ID = -1002815033595  # Обратите внимание: минус и без кавычек!

# URL вашего Mini App
WEB_APP_URL = "https://ghostly-singular-seriema.cloudpub.ru/"

# Проверка подписки
def is_user_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_subscribed(user_id):
        show_app_button(message)
    else:
        show_subscription_prompt(message)

# Функция показа кнопки Mini App
def show_app_button(message):
    markup = types.InlineKeyboardMarkup()
    web_app_button = types.WebAppInfo(url=WEB_APP_URL)
    markup.add(types.InlineKeyboardButton(text="📱 Открыть приложение", web_app=web_app_button))
    bot.reply_to(message, "Добро пожаловать! Нажмите на кнопку ниже:", reply_markup=markup)

# Сообщение о необходимости подписки
def show_subscription_prompt(message):
    markup = types.InlineKeyboardMarkup()
    subscribe_btn = types.InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/SchoolGPTtest")
    check_btn = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subscription")
    markup.add(subscribe_btn)
    markup.add(check_btn)
    bot.reply_to(message, "Подпишитесь на наш канал, чтобы использовать бота 👇", reply_markup=markup)

# Callback для повторной проверки
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    if is_user_subscribed(user_id):
        bot.answer_callback_query(call.id, "Вы подписаны!", show_alert=True)
        show_app_button(call.message)
    else:
        bot.answer_callback_query(call.id, "Вы всё ещё не подписаны.", show_alert=True)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)