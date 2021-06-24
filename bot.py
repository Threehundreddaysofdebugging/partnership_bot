import json

import telebot
from telebot import types

# -*- coding: utf-8 -*-

with open('TOKEN.txt') as t:
    TOKEN = t.readline()

bot = telebot.TeleBot(TOKEN)

user_step = {}

@bot.message_handler(commands=['start'])
def start(message):
    send_mess = "<b>Здравствуйте! Я был создан для покупки и продажи услуг в социальной сети Twiter." \
                " Вот что я умею:</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')
    help(message)
    user_step[message.chat.id] = -2


@bot.message_handler(commands=['sell'])
def sell(message):
    send_mess = "Ознакомьтесь с правилами для одобрения заявки, а затем представтесь."
    user_step[message.chat.id] = 1
    bot.send_message(message.chat.id, send_mess)
    rule(message)
    user_step[message.chat.id] = -1


@bot.message_handler(commands=['feedback'])
def feedback(message):
    send_mess = "Для обратной связи обратитесь к @аккаунт главного модератора"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['buy'])
def buy(message):
    send_mess = "///"
    bot.send_message(message.chat.id, send_mess, parse_mode='html') 

@bot.message_handler(commands=['cooper'])
def cooper(message):
    markup1 = types.InlineKeyboardMarkup()
    rov = types.InlineKeyboardButton(text='РОВЕРЗЕТ', url='https://twitter.com/roverzet')
    markup1.add(rov)
    send_mess = "С нами сотрудничают:"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup1)


@bot.message_handler(commands=['rules'])
def rule(message):
    send_mess = "Правила для одобрения заявки модераторами: 1. Отсутствие экстремистских высказываний. " \
                "\n2. Твит без высказываний с разжиганием ненависти. \n" \
                "3. Твит не должен содержать порнографические материалы. Если ваша заявка будет отклонена, " \
                "то вы будете оповещены об этом."
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    send_mess = "Я был создан для покупки ретвитов и лайков у популярных твиттерских. Если вы покупаете услугу," \
                " то вы должны подать заявку с указанием точного твита и действий с ним. Заявка будет рассмотрена " \
                "модераторами и при одобрении будет предлагаться твиттерским некоторое время, после чего будет" \
                " деактивирована. Если вы продаете услугу, то ваш аккаунт должен быть подтвержден. Для подтверждения" \
                " вам следует иметь не менее /сколько то/ тысяч подписчиков и обратиться к модераторам бота со всеми" \
                " доказательствами. Если ваш аккаунт подтвержден, то вам будет доступен раздел покупок и вы сможете" \
                " просматривать заявки. Бот не требует пароль от вашего аккаунта. Для обратной связи и предложений," \
                " а также подтверждения аккаунта, напишите /feedback Для правил по которым происходит рассмотрение " \
                "заявки введите /rules"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


def introduce(message):
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    users[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Вы благополучно зарегестрированы. Отправьте ссылку на рекламируемый твит')
    with open('users.json', 'w') as f:
        json.dump(users, f)
    user_step[message.chat.id] = 1


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
#    markup = types.InlineKeyboardMarkup(row_width=1)
#    retweet = types.InlineKeyboardButton('Ретвит', callback_data='retweet0')
#    like = types.InlineKeyboardButton('Лайк', callback_data='like0')
#    sub = types.InlineKeyboardButton('Подписка на автора', callback_data='sub0')
#    tweet = types.InlineKeyboardButton('Твит', callback_data='tweet0')
#    markup.add(retweet, like, sub, tweet)

    try:
        with open('tweets and actions.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    users[message.chat.id] = message.text
    if user_step[message.chat.id] == -1:
        introduce(message)
        return
    elif user_step[message.chat.id] != 1:
        bot.send_message(message.chat.id, 'Не так быстро, для начала вызовите  нужную вам команду.')
        return
    elif "https://twitter.com/" in message.text:  # TODO проверка на существование твита
        bot.send_message(message.from_user.id, "Введите действие. Возможные действия: Ретвит, Лайк, Твит, Подписка.")
    elif "https://mobile.twitter.com/" in message.text: 
        bot.send_message(message.from_user.id, "Введите действие. Возможные действия: Ретвит, Лайк, Твит, Подписка.")  

    elif "Лайк" in message.text: 
        bot.send_message(message.from_user.id, "Ваша заявка принята в обработку.") 
    elif "Твит" in message.text: 
        bot.send_message(message.from_user.id, "Ваша заявка принята в обработку.")  
    elif "Ретвит" in message.text: 
        bot.send_message(message.from_user.id, "Ваша заявка принята в обработку.") 
    elif "Подписка" in message.text: 
        bot.send_message(message.from_user.id, "Ваша заявка принята в обработку.") 
    else:
        bot.send_message(message.chat.id, 'Это не корректная ссылка, либо действие. Попробуйте снова.')
    with open('tweets and actions.json', 'w') as f:
        json.dump(users, f)
        user_step[message.chat.id] = 1

try:
    bot.polling(none_stop=True)
except Exception:
    pass
