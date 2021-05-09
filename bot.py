import telebot
from decouple import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


'''Создание кнопок'''
inline_key_yes_no = InlineKeyboardMarkup()
btn_yes = InlineKeyboardButton('Да', callback_data='yes')
btn_no = InlineKeyboardButton('Нет', callback_data='no')
inline_key_yes_no.add(btn_yes, btn_no)

bot = telebot.TeleBot(config('TOKEN'))

@bot.message_handler(commands=['play',])
def welcome(message):
    msg = bot.send_message(message.chat.id, 'Welcome dude!')
    start_game(msg)

def start_game(message):
    bot.send_message(message.chat.id, 'Do you wanna play?', reply_markup=inline_key_yes_no)

@bot.callback_query_handler(func=lambda c:True)
def callback_inline(c):
    if c.data == 'yes':
        msg = bot.send_message(c.message.chat.id, 'choose integer in range 1-100')
        '''начать игру'''
        bot.register_next_step_handler(msg, game)

    if c.data == 'no':
        bot.send_message(c.message.chat.id, 'bye')
        '''стикер'''
        bot.send_sticker(c.message.chat.id, 'CAACAgIAAxkBAAEBOnFgiTMHZB01uN6aAAG9TfKssXE4-qgAAkMAAyRxYhoNKXOTluNPrR8E')

'''игра'''
def game(message):
    import random
    num = int(random.randint(1,101))
    print(num)      # число, которое выбрал бот
    tries = 5
    '''логика игры'''
    def body(message):
        guess = int(message.text)    # число, которое выбрал пользователь
        nonlocal tries
        if guess == num:
            bot.send_message(message.chat.id, 'Congrats! You won!')
            tries-=1
            bot.send_message(message.chat.id, f'it took you {5 - tries} tries')
            '''начать заново'''
            start_game(message)
        elif tries == 1:
            bot.send_message(message.chat.id, 'sorry, game over')
            '''начать заново'''
            start_game(message)
        elif guess > num:
            tries -= 1
            bot.send_message(message.chat.id, 'try lower number')
            msg = bot.send_message(message.chat.id, f'you have {tries} tries left')
            '''новая попытка'''
            bot.register_next_step_handler(msg, body)
        elif guess < num:
            tries -= 1
            bot.send_message(message.chat.id, 'try bigger number')
            msg = bot.send_message(message.chat.id, f'you have {tries} tries left')
            '''новая попытка'''
            bot.register_next_step_handler(msg, body)

    '''запустить игру в 1 раз'''
    body(message)

bot.polling(none_stop=True)