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
    bot.send_message(message.chat.id, "Представьтесь и вы!", parse_mode='html')

    user_step[message.chat.id] = -1


@bot.message_handler(commands=['back'])
def back(message):
    # TODO возврат на предыдущий шаг или в начало
    if user_step[message.chat.id] > 0:
        user_step[message.chat.id] -= 1


@bot.message_handler(commands=['sell'])
def sell(message):
    if user_step[message.chat.id] != 0:
        bot.send_message(message.chat.id, 'Не так быстро, для начала предствьтесь!')
        return
    send_mess = "Ознакомьтесь с правилами для одобрения заявки, а затем отправьте ссылку на ваш твит."
    user_step[message.chat.id] = 1
    bot.send_message(message.chat.id, send_mess)
    bot.send_message(message.chat.id, 'Правила:')
    rule(message)


@bot.message_handler(commands=['feedback'])
def feedback(message):
    send_mess = "Для обратной связи обратитесь к @аккаунт главного модератора"
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
    bot.send_message(message.chat.id, 'Вы благополучно зарегестрированы. Отправьте ссылку на рекламируемый твит и действие с ним в формате:'\
        ' https://twitter.com/user/0123456789876543210 Лайк'\
        '              Возможные действия: Ретвит, Лайк, Твит, Подписка.')
    with open('users.json', 'w') as f:
        json.dump(users, f)
    user_step[message.chat.id] = 1


def is_correct_link(link):
    user_id = link.split('status')[-1][1:20]



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
#    markup = types.InlineKeyboardMarkup(row_width=1)
#    retweet = types.InlineKeyboardButton('Ретвит', callback_data='retweet0')
#    like = types.InlineKeyboardButton('Лайк', callback_data='like0')
#    sub = types.InlineKeyboardButton('Подписка на автора', callback_data='sub0')
#    tweet = types.InlineKeyboardButton('Твит', callback_data='tweet0')
#    markup.add(retweet, like, sub, tweet)
    moder_id = 1802110885

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
        bot.send_message(message.chat.id, 'Не так быстро, для начала вызовите команду /sell')
        return
    elif "https://twitter.com/" in message.text or "https://mobile.twitter.com/" in message.text:
        # TODO проверка на существование твита
        with open('users.json', 'r') as f:
            users = json.load(f)
        bot.send_message(message.from_user.id, "Ваша заявка принята в обработку.")
        bot.send_message(moder_id, f'{users[message.chat.id]}\n{message.text}\n')
    else:
        bot.send_message(message.chat.id, 'Это не корректная ссылка, попробуйте другую')
    with open('tweets and actions.json', 'w') as f:
        json.dump(users, f)
        user_step[message.chat.id] = 1


@bot.message_handler(commands=['buy'])
def buy(message):
    markup3 = types.InlineKeyboardMarkup(row_width=1)
    tweet = types.InlineKeyboardButton('Продолжить', callback_data='con')
    markup3.add(con)

    send_mess = "Для продолжения, ваш аккаунт должен быть подтвержден. Для подтверждения обратитесь к модератору по команде /feedback. Если ваш аккаунт уже подтвержден, просто нажмите кнопку ниже."
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup3)


try:
    bot.polling(none_stop=True)
except Exception:
    pass
