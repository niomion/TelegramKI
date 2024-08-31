import telebot
from datetime import datetime
import pytz
from flask import Flask

app = Flask(__name__)

TOKEN = "7542022559:AAFpP7-ZId3x0aFon8OGGlTcnzNeZ1Jp42s"
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return "Telegram bot is running!"

@bot.message_handler(commands=['test'])
def send_welcome(message):
    timezone = pytz.timezone("Europe/Kiev")
    local_time = datetime.now(timezone)
    nowis = "Привіт, зараз саме такий час: " + local_time.strftime('%Y-%m-%d %H:%M:%S')
    bot.reply_to(message, nowis)

# Запускаємо бота
bot.polling(non_stop=True, interval=0)

# Запускаємо Flask сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
