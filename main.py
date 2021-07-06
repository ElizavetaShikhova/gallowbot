# -*- coding: utf-8 -*-
import telebot
from random import choice

bot = telebot.TeleBot("1692103063:AAFODa86dMYsUBAl27LFGZLOOJq_LpQU2u0", parse_mode=None)

user_info = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    im_a_boss(message.from_user.id)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = telebot.types.KeyboardButton('Начать игру')
    button_rules = telebot.types.KeyboardButton('Правила игры')
    markup.add(button_start, button_rules)
    bot.send_message(message.chat.id, 'Нажми на одну из кнопок', reply_markup=markup)
    user_info[message.from_user.id] = ['','',-1,list()]

@bot.message_handler(func=lambda m: True)
def send_letters(message):
    global user_info
    user_id = message.from_user.id

    def morphology(n):
        if n > 4:
            return 'попыток'
        if n < 5 and n > 1:
            return 'попытки'
        return 'попытка'

    def print_mes(f):
        global user_info
        if f == 0:
            bot.send_message(message.chat.id,
                             f"Такой буквы нет в слове, упс :(\nУ тебя осталось {user_info[user_id][2]} {morphology(user_info[user_id][2])}\n{pr_word()}")
            bot.send_photo(message.chat.id, pic())
            user_info[user_id][2] -= 1
        elif f == 1:
            bot.send_message(message.chat.id, f"Ты отгадал слово {ans_word()}!Поздравляю, ты крутой")
            user_info[user_id][2] = -1
        elif f == 2:
            bot.send_message(message.chat.id, f"Эта буква есть в слове!\U0001F609\n{pr_word()}")
        elif f == 3:
            bot.send_message(message.chat.id, f"Игра окончена, ты не справился \U0001F62D\nЭто было слово {user_info[user_id][0]}")
            bot.send_photo(message.chat.id, 'https://sun9-48.userapi.com/impg/QXXzoibocuexYpsCmNGPTDal7-RFSZnYiJNjtg/DKJ4psqu4HI.jpg?size=144x144&quality=96&sign=4d130882dfa786ecf95b62536162e7bc&type=album')
            user_info[user_id][2] = -1
        elif f == 4:
            bot.send_message(message.chat.id, f"Ты не в игре. Напиши /start")
        elif f == 5:
            bot.send_message(message.chat.id, f'Ты уже нажимал на эту букву')

    def ans_word():
        global  user_info
        if len(user_info) > 60:
            user_info = {}
        user_id = message.from_user.id
        user_word = user_info[user_id][1]
        word = user_info[user_id][0]
        user_n = user_info[user_id][2]
        user_letters = user_info[user_id][3]
        for i in range(1, len(user_word) - 1):
            if user_word[i] == '_' and message.text == word[i]:
                user_word[i] = message.text
        user_info[user_id] = [word, user_word,user_n, user_letters]
        return word

    def pr_word():
        global user_info
        user_id = message.from_user.id
        user_word = user_info[user_id][1]
        word = user_info[user_id][0]
        prword = word[0]
        for i in range(1, len(user_word) - 1):
            if user_word[i] != '_':
                prword += user_word[i]
            else:
                prword += ' _ '
        prword += word[-1]
        return prword

    def pic():
        user_id = message.from_user.id
        user_n = user_info[user_id][2]
        with open('pic.txt') as f:
            lines = f.readlines()
            return lines[user_n]


    if message.text == 'Начать игру':
        n = 10
        user_id = message.from_user.id
        word = choice(list(open('dictionary.txt',encoding='utf-8')))[:-1]
        user_word = list(word[0] + ('_' * (len(word) - 2)) + word[-1])
        user_info[user_id] = [word, user_word, n, list()]
        prword = word[0] + (' _ ' * (len(word) - 2)) + word[-1]
        bot.send_message(message.chat.id, f"Привет. Я загадал слово:\n{prword}\nНапиши любую букву")

    elif message.text == 'Правила игры':
        bot.send_message(message.chat.id, f"Суть игры достаточно банальна и проста - называя буквы, "
                                          f"угадать слово. Игрок предлагает буквы, которые он считает "
                                          f"могут входить в слово. Если он угадывает букву, то бот "
                                          f" отображает ее (или их, если таких букв в слове "
                                          f"несколько) в соответствующем месте. Если буква в слове "
                                          f"отсутствует, то к виселице пририсовывается часть человека."
                                          f"Игрок может назвать слово целиком, но на это у него одна попытка.В момент, "
                                          f"когда человек будет нарисован полностью, "
                                          f"игра заканчивается проигрышем")
    elif user_info[user_id][2] > 0:
        user_id = message.from_user.id
        word = user_info[user_id][0]
        message.text = message.text.lower()
        if len(message.text) == 1:
            if message.text in user_info[user_id][3]:
                print_mes(5)
            elif message.text in word:
                user_info[user_id][3].append(message.text)
                ans_word()
                prword = pr_word()
                if prword != word:
                    print_mes(2)
                else:
                    print_mes(1)
            else:
                user_info[user_id][3].append(message.text)
                print_mes(0)
        else:
            if message.text == word:
                print_mes(1)
            else:
                print_mes(3)
    elif user_info[user_id][2] == 0:
        print_mes(3)
    elif user_info[user_id][2] == -1:
        print_mes(4)


bot.polling(none_stop=True, interval=0)