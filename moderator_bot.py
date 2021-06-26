
import telebot

with open('MODER_TOKEN.txt') as t:
    TOKEN = t.readline()

bot = telebot.TeleBot(TOKEN)
# будет получать сообщения от первого бота и пересылать их модераторам-людям


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.is_bot:
        return
    bot.send_message(message.user.id, 'hi')

@bot.message_handler(content_types=['text'])
def text(message):
    bot_name = '@twibuysellbot'
    moderators = ['@swen13066', 'drakoneans']
    if message.from_user.username == bot_name:
        bot.forward_message(moderators[0], bot_name, message.message_id)
    if message.from_user.username in moderators:
        msg_id = message.reply_to_mesage.forward_from_message_id
        bot.send_message(bot_name, f'{msg_id}\n{1 if message.text == "1" else 0 }')
    else:
        bot.send_message(message.chat.id, 'ТЫ НЕ РОВЕРЗЕТ')



bot.polling()
