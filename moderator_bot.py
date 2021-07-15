# -*- coding: utf-8 -*-
import telebot

from misc import *

with open('storage/MODER_TOKEN.txt') as t:
    TOKEN = t.readline()

moderators = ['swen13066']

bot = telebot.TeleBot(TOKEN)
bot.get_updates(allowed_updates=["channel_post", 'message'])


def moder():
    return 680890776


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.id in get_all_advertisers_id():
        if message.text == 'done':
            pass
    elif message.from_user.username in moderators:
        repl_message = message.reply_to_message
        user_id = get_user_id(repl_message.text.split('\n')[0][12:])
        if message.text.lower() == 'ok':
            approve(user_id, True)
            task = get_task(user_id)
            for ader in task.advertisers:
                name, link, action = take_data(user_id)
                bot.send_message(ader.id, f'brand name: {name}\nlink: {link}\naction: {action}')
        elif message.text == 'not':
            approve(user_id, False)

        bot.send_message(-1001514844359, user_id)
    else:
        bot.send_message(message.chat.id, 'ТЫ НЕ РОВЕРЗЕТ')


@bot.channel_post_handler()
def text_post(message):
    name, link, action = take_data(message.text)

    bot.send_message(moder(), f'brand name: {name}\nlink: {link}\naction: {action}')


db_session.global_init("db/twee.db")
print('запущен')
bot.polling()
