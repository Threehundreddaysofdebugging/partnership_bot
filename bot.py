import telebot
from telebot import types
import tweepy
import math
# -*- coding: utf-8 -*-

with open('TOKEN.txt') as t:
	TOKEN = t.readline()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
	send_mess = "<b>Здравствуйте! Данный бот был создан для покупки и продажи услуг в социальной сети Twiter. Для более подробной информации и инстуркции в использовании напишите</b> /help"
	bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['sell'])
def sell(message):
	send_mess = "Ознакомьтесь с правилами для одобрения заявки, а затем отправьте ссылку на ваш твит."
	bot.send_message(message.chat.id, send_mess)

@bot.message_handler(commands=['feedback'])
def feedback(message):
	send_mess = "Для обратной связи обратитесь к @аккаунт главного модератора"
	bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands = ['cooper'])
def cooper(message):
    markup1 = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='РОВЕРЗЕТ', url='https://twitter.com/roverzet?s=20')
    markup1.add(btn_my_site)
    bot.send_message(message.chat.id, "С нами сотрудничают:", parse_mode='html', reply_markup = markup1)

@bot.message_handler(commands=['rules'])
def rule(message):
	send_mess = "Правила для одобрения заявки модераторами: 1. Отсутствие экстремистских высказываний. 2. Твит без высказываний с разжиганием ненависти. 3. Твит не должен содержать порнографические материалы."
	bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
	send_mess = "Данный бот был создан для покупки ретвитов и лайков у популярных твиттерских. Если вы покупаете услугу, то вы должны подать заявку с указанием точного твита и действий с ним. Заявка будет рассмотрена модераторами и при одобрении будет предлагаться твиттерским три дня, после чего будет деактивирована. Если вы продаете услугу, то ваш аккаунт должен быть подтвержден. Для подтверждения вам следует иметь не менее тысячи подписчиков и обратиться к модераторам бота со всеми доказательствами. Если ваш аккаунт подтвержден, то вам будет доступен раздел покупок и вы сможете просматривать заявки. Бот не требует пароль от вашего аккаунта. Для обратной связи и предложений, а также подтверждения аккаунта, напишите /feedback Для правил по которым происходит рассмотрение заявки введите /rules"
	bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text == "https://twitter.com/":
   		bot.send_message(message.from_user.id, "Выберите действие, которое следует выполнить с твитом:", reply_markup=markup)
  
markup = types.InlineKeyboardMarkup(row_width=1)
retweet = types.InlineKeyboardButton('Ретвит', callback_data='retweet0')
like = types.InlineKeyboardButton('Лайк', callback_data='like0')
sub = types.InlineKeyboardButton('Подписка на автора', callback_data='sub0')
markup.add(retweet, like, sub)

bot.polling(none_stop=True)
