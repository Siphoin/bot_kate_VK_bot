# Импорт библиотек и py скриптов

import vk_api
import datetime
from datetime import date
import requests
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
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
   ###


# Отправка сообщение пользователю
# id - id пользователя, который отправил нам сообщение
# message - сообщение, которое нужно отправить в ответ


def sendMessage (id, messsge):
    vk_session.method("messages.send", {"user_id": id, "message": messsge, "random_id": 0})


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
          if msg == "курс валют":
              showExchangeRate()
          if msg == "сколько сейчас времени?":
              showTime()