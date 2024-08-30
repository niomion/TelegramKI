import telebot

TOKEN = "7542022559:AAFpP7-ZId3x0aFon8OGGlTcnzNeZ1Jp42s"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['test'])
def send_welcome(message):
    bot.reply_to(message, "Hello World!")

# Запускаємо бота
bot.polling()