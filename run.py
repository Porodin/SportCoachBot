import requests
import telebot

from aiogram import Dispatcher
from telebot import types
from bs4 import BeautifulSoup
Token_API = "6645247048:AAFYx8UJ9A8oDyFnBVHbJ8uVntpBTyBYNEE"

bot = telebot.TeleBot(Token_API)

dp = Dispatcher()
#Обработчик событий

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("🙂да")
button2 = types.KeyboardButton("😔нет")

markup.add(button1, button2)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f'Приветствую тебя, {message.from_user.first_name}! Я бот, который позволит тебе выбрать товар, по интересующей тебя категории в таких интернет-магазинах как:<b> <a href="https://www.sportmaster.ru"> Спортмастер</a></b>, <b> <a href="https://www.ozon.ru">Ozon</a></b>, <b> <a href="https://www.wildberries.ru">Wildberries</a></b>'
    'Открыть список категорий?',
    parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def choiceandparcing(message):
    if message.chat.type == 'private':
        if message.text == '🙂да':
           markup = types.InlineKeyboardMarkup(row_width=2)
           button1 = types.InlineKeyboardButton('гантели', callback_data='dumbbells')
           button2 = types.InlineKeyboardButton('грифы', callback_data='rods')
           button3 = types.InlineKeyboardButton('эспандеры', callback_data='expanders')
           button4 = types.InlineKeyboardButton('гири', callback_data='weights')
           markup.add(button1, button2, button3, button4)
           bot.send_message(message.chat.id, 'выберите категорию товара', reply_markup=markup)
        elif message.text == '😔нет':
          bot.send_message(message.chat.id, 'Значит в другой раз')
        else:
          bot.send_message(message.chat.id, 'Не знаю, что ответить')

@bot.callback_query_handler(func=lambda call:True)
def collback_inline(call):
    print('')
    if call.message:
        print(call.data)
        if call.data == 'dumbbells':
            print(1)
            link = "https://www.sportmaster.ru/"
            url = "https://www.sportmaster.ru/catalog/vidy_sporta_/trening/svobodnyy_ves/"
            responce = requests.get(url)
            soup = BeautifulSoup(responce.text, "html.parser")
            section = soup.find_all("div", class_="sm-product-grid sm-product-grid--size-xs")
            for products in section:
                product = products.find_all("div", class_="product-card")
                for item in product:
                    product_name = item.find("span", class_="car-block-title").get_text(strip=True)
                    product_price = item.find("div", class_="price hvr-sweep-to-right").get_text(strip=True)
                    product_link = link + item.find("a", class_="product_list_img").get("href")
                    all_poducts = f"{product_name}\n Цена: {product_price}\n Ссылка: {product_link}"
                    bot.send_message(call.message.chat.id, all_poducts)










bot.polling(none_stop=True)
