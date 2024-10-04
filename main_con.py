import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('7296658984:AAG4LiKFaz__tHbmZTFw4OjSRmN4Ag3pcDE')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, write count')
    bot.register_next_step_handler(message, summa)



def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid format, please enter the amount')
        bot.register_next_step_handler(message, summa)
        return


    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Enother count', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Write some currency', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'The number must be greater than 0, write count')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result: {round(res, 2)}. You cen rewrite count.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Enter a pair of numbers separated by a slash')
        bot.register_next_step_handler(call.message, my_currency)



def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)}. You cen rewrite count.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Somthings wrong. Enter the value again')
        bot.register_next_step_handler(message, summa)

bot.polling(none_stop=True)