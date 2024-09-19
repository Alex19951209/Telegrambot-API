import telebot
import requests
import json

bot = telebot.TeleBot('7296658984:AAG4LiKFaz__tHbmZTFw4OjSRmN4Ag3pcDE')
API = '302456f485b002c8b5c4c901c0eae2c0'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi, nice to see you! Write please city's name!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f'Weather now: {data["main"]["temp"]}')

        image = 'sun.jpeg' if temp > 22.0 else 'rain.png'
        file = open('./' +image,'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'The city is not correct.')

bot.polling(none_stop=True)