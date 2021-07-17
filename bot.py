# -*- coding: utf-8 -*-
import telebot
from telebot import types

from misc import *

with open('storage/TOKEN.txt') as t:
    TOKEN = t.readline()

with open('storage/SHOPID.txt') as s:
    SHOPID = s.readline()

bot = telebot.TeleBot(TOKEN)
bot.get_updates(allowed_updates=["channel_post", 'message'])

user_step = {}


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = "<b>Здравствуйте! Я был создан для покупки и продажи услуг в социальной сети Twitter." \
                " Вот что я умею:</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')
    help(message)
    user_step[message.chat.id] = 0


@bot.message_handler(commands=['back'])
def back(message):
    if user_step[message.chat.id] > 1:
        user_step[message.chat.id] -= 1


@bot.message_handler(commands=['sell'])
def sell(message):
    if is_registered(message.chat.id):
        user_step[message.chat.id] = 12
        bot.send_message(message.chat.id, 'вы уже зарегестрированы')
    else:
        user_step[message.chat.id] = 11
        bot.send_message(message.chat.id, 'для регистрации введите ваш username в твиттере')


@bot.message_handler(commands=['rules'])
def rule(message):
    send_mess = "Правила для одобрения заявки модераторами: 1. Отсутствие экстремистских высказываний. " \
                "\n2. Твит без высказываний с разжиганием ненависти. \n" \
                "3. Твит не должен содержать порнографические материалы. Если ваша заявка будет отклонена, " \
                "то вы будете оповещены об этом."
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['buy'])
def buy(message):
    if is_introduced(message.chat.id):
        user_step[message.chat.id] = 2
        t = 'Мы с вами уже знакомы, но ознакомьтесь с правилами для одобрения заявки на всякий случай'
        bot.send_message(message.chat.id, t)
        rule(message)
    else:
        user_step[message.chat.id] = 1
        t = 'предствьтесь, пожалуйста'
        bot.send_message(message.chat.id, t)


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


def is_correct_link(link):
    user_id = link.split('status')[-1][1:20]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    action = 0
    if user_step[message.chat.id] == 0:
        bot.send_message(message.chat.id, 'Не так быстро, для начала вызовите нужную вам команду.')
    elif user_step[message.chat.id] == 1:
        introduce(message)
        bot.send_message(message.chat.id, 'Вы благополучно зарегестрированы. Отправьте ссылку на рекламируемый твит')
        user_step[message.chat.id] = 2
    elif user_step[message.chat.id] == 2:
        if "https://twitter.com/" in message.text or "https://mobile.twitter.com/" in message.text:
            # TODO проверка на существование твита
            add_link_to_task(message.chat.id, message.text)

            bot.send_message(message.from_user.id,
                             "Введите действие. Возможные действия: Ретвит, Лайк, Твит, Подписка.")
            user_step[message.chat.id] = 3
        else:
            bot.send_message(message.chat.id, 'Это не корректная ссылка, попробуйте другую')
    elif user_step[message.chat.id] == 3:
        m = message.text.lower().strip()
        if m in ["лайк", "ретвит", "подписка"]:
            action = m
        else:
            bot.send_message(message.chat.id, 'Это не корректное действие, попробуйте еще раз')
            return
        add_action_to_task(message.chat.id, action)
        bot.send_message(message.chat.id, 'ader choise')
        user_step[message.chat.id] = 4
    elif user_step[message.chat.id] == 4:
        add_advertisers_to_task(message.chat.id, message.text.split('\n'))

        # TODO заявка на оплату
        #    bot.send_invoice(message.chat.id, 'title', 'description', 0,
        #                  SHOPID, 'RUB', 0)
        user_step[message.chat.id] = 5
    elif user_step[message.chat.id] == 5:
        bot.send_message(-1001514844359, f'{message.chat.id}')

    elif user_step[message.chat.id] == 11:
        register(message)
        bot.send_message(message.chat.id, 'зарегестрировано\nданные для начисления')
        user_step[message.chat.id] = 12
    elif user_step[message.chat.id] == 12:
        #TODO обработка банковских данных
        bot.send_message(message.chat.id, 'u available')
        make_available(message.chat.id)




@bot.channel_post_handler(content_types=['text'])
def text_post(message):
    if is_approved(message.text):
        t = 'подтвержден'
    else:
        t = 'не подтвержден'
    bot.send_message(message.text, t)


db_session.global_init("db/twee.db")
print('я работаю')
bot.polling(none_stop=True)
