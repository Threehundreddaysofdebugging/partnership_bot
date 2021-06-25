import telebot

with open('MODER_TOKEN.txt') as t:
    TOKEN = t.readline()

bot = telebot.TeleBot(TOKEN)
# будет получать сообщения от первого бота и пересылать их модераторам-людям


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi')

bot.polling()