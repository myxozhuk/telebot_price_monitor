import requests
import telebot
from bs4 import BeautifulSoup
bot = telebot.TeleBot('2049517751:AAFhBBidOVQdIroC86h3kMjwQBI5QLPH8uk')
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, я помощник по поиску и отслеживанию цен на товары. Напиши /help, чтобы получить подсказку")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/add - добавить новый товар для отслеживания.")
    elif message.text == '/add':
        bot.send_message(message.from_user.id, "Какой товар вы хотите добавить в список?")
        bot.register_next_step_handler(message, add_product) #следующий шаг – функция add_product
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def add_product(message):
    global product
    product = message.text
    product = product.replace(" ", "+")
    url = "https://www.e-katalog.ru/ek-list.php?katalog_=189&search_=" + product
    r = requests.get(url)
    page = r.text
    # print(page)
    soup = BeautifulSoup(page, 'html.parser')
    tag_div = soup.find("div", class_="model-price-range")
    strings = tag_div.text.split()
    low_price = strings[1] + strings[2]
    high_price = strings[4] + strings[5]
    bot.send_message(message.from_user.id, 'Товар добавлен. Самая низкая цена: '+ low_price)

bot.polling()