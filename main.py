# Импорт библиотек и py скриптов

import vk_api
import datetime
from datetime import date
import requests
import string
import random
import sys
from vk_api.longpoll import VkLongPoll, VkEventType
from tk import tkValue
from exchange_rate import DOLLAR_URL
from exchange_rate import RUB_URL
from exchange_rate import GRUVNA_URL
from exchange_rate import HEADERS
from bs4 import BeautifulSoup
###

   # Создаем сессию VK API
vk_session = vk_api.VkApi(token=tkValue)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
   ###


# Отправка сообщение пользователю
# id - id пользователя, который отправил нам сообщение
# message - сообщение, которое нужно отправить в ответ


def sendMessage (id, text):
    vk.messages.send(user_id = id, message = text, random_id = 0)


###

# Отправка стикера пользователю
# id - кому отправляется стикер
# stik_id - id стикера


def sendStick (id, stik_id):
    vk.messages.send(user_id = id, sticker_id = stik_id, random_id = 0)
    ###

    ### Отправляет пользователю случайное число
def generateNumber (id):
    msg = str(random.randint(-2147483647, 2147483647))
    sendMessage(id, msg)
    ###
   

   ### Генерирует пароль пользователю


def sendGeneratedPassword(id):
    msg = ""
    count_symbols = random.randint(16, 32)
    for number in range(count_symbols):
        msg += str(chr(random.randint(0, 135)))
    sendMessage(id, msg)

    ###

    
### Отправляет пользователю шаблон HTML файла


def generateHTMLExample(id):
    f = open("example_html_text.txt")
    text =   f.read()
    f.close()
    sendMessage(id, text)
    ###
### Отвечает пользователю на его приветствие
def helloMessage(id):
    msg = ""
    num = random.randint(1, 2)
    if num == 1:
        msg = "Привет!"
    if num == 2:
        msg = "Привет! Как дела?"
        sendStick(id, 1)
    sendMessage(id, msg)
###

def showExchangeRate():
    # Получаем текущую дату сервера

    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    ###


#   Получаем курс доллара к рублю


    full_page = requests.get(DOLLAR_URL, headers=HEADERS)
    soup = BeautifulSoup(full_page.content, "html.parser")
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    dollarValue = convert[0].text
   # Получаем курс рубля к доллару


    full_page = requests.get(RUB_URL, headers=HEADERS)
    soup = BeautifulSoup(full_page.content, "html.parser")
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 3})
    rubVaLUE = convert[0].text
    ###

    # Получаем курс доллара к гривне


    full_page = requests.get(GRUVNA_URL, headers=HEADERS)
    soup = BeautifulSoup(full_page.content, "html.parser")
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    gruvnaValue = convert[0].text
    ###


# Отправляем данные о курсе


    data =  "Данные ЦБ от " + date_string + "\n1 доллар США: = " + dollarValue + " ₽\n1 ₽ = " + rubVaLUE + " $\n1 гривна = " + gruvnaValue + " $"
    sendMessage(id, data)
    ###

# Отправляем пользователю текущее время сервера
def showTime():
    now = datetime.datetime.now()
    sendMessage(id, now.strftime("%H:%M"))
    # Прослушиваем пользователей
for event in longpoll.listen():
    
    if event.type == VkEventType.MESSAGE_NEW:
      if  event.to_me:
          msg = event.text.lower()
          id = event.user_id
          if msg == "случайное число":
              generateNumber(id)
          if msg == "сгенерируй шаблон html" or msg == "сгенерируй html":
              generateHTMLExample(id)
          if msg == "сгенерируй пароль":
              sendGeneratedPassword(id)
          if msg == "привет":
              helloMessage(id)
          if msg == "курс валют":
              showExchangeRate()
          if msg == "сколько сейчас времени?":
              showTime()