import os
from telebot import types
from keyboard import keys_admin,keys_menu

path = "C:/Users/smehn/PycharmProjects/Predatory Beavers Bot/gifts"


def add(message, bot):
    with open("gifts/{count}.txt".format(count=len(os.listdir(path)) + 1), 'w+', encoding="utf-8") as fileW:
        if message.chat.last_name != None:
            print(f"Отправитель: {message.chat.first_name} {message.chat.last_name}", file=fileW)
        else:
            print(f"Отправитель: {message.chat.first_name}", file=fileW)
        print(message.text, file=fileW)
    bot.send_message(message.chat.id, "Твое сообщение уже доставлено игрокам ❤️‍🔥\n\nБлагодарим!", reply_markup=keys_menu)


def get(message, bot):
    if len(os.listdir(path)) > 0:
        for gift in os.listdir(path):
            with open(f"gifts/{gift}", "r", encoding="utf-8") as fileR:
                keys_gift = types.InlineKeyboardMarkup()
                keys_gift.add(types.InlineKeyboardButton(text="Y", callback_data="gift_yes"))
                keys_gift.add(types.InlineKeyboardButton(text="N", callback_data="gift_no"))
                bot.send_message(message.chat.id, fileR.read(), reply_markup=keys_gift)
    else:
        bot.send_message(message.chat.id, "Новых пожеланий нет")


def reply_to(message, bot):
    bot.send_message(-1002120616869, f"{message.text}")
    remove(message)


def remove(message):
    filepath = ""
    for gift in os.listdir(path):
        with open(f"gifts/{gift}", "r", encoding="utf-8") as fileR:
            if fileR.read() == message.text + '\n':
                filepath = "C:/Users/smehn/PycharmProjects/Predatory Beavers Bot/" + fileR.name
        fileR.close()
    os.remove(filepath)