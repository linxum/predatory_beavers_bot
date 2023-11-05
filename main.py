import telebot
from telebot import types
import mailing

token = "6578454575:AAE9ZgatzU730m4vslDHJqgQu8ayAYsHkDo"
channel_id = "@predatorybeaver"

bot = telebot.TeleBot(token)
keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Написать напутствие")


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Добро пожаловать в бот!")
    if is_subscribed(channel_id, message.from_user.id):
        key_subscribe = types.ReplyKeyboardMarkup(True, True)
        key_subscribe.add("Проверить подписку")

        get_link = types.InlineKeyboardMarkup()
        get_link.add(types.InlineKeyboardButton(text="PREDATORY BEAVERS", url="https://t.me/predatorybeaver"))

        bot.send_message(message.chat.id, "Ссылка на канал", reply_markup=get_link)
        bot.send_message(message.chat.id, "Для работы с ботом вам необходимо подписаться на наш канал!",
                         reply_markup=key_subscribe)


def is_subscribed(channel_id, user_id):
    try:
        bot.get_chat_member(channel_id, user_id)
        return True
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


@bot.message_handler(content_types=['text'])
def keys(message):
    if message.text == "Проверить подписку":
        if is_subscribed(channel_id, message.from_user.id):
            key_subscribe = types.ReplyKeyboardMarkup(True, True)
            key_subscribe.add("Проверить подписку")

            get_link = types.InlineKeyboardMarkup()
            get_link.add(types.InlineKeyboardButton(text="PREDATORY BEAVERS", url="https://t.me/predatorybeaver"))

            bot.send_message(message.chat.id, "Ссылка на канал", reply_markup=get_link)
            bot.send_message(message.chat.id, "Для работы с ботом вам необходимо подписаться на наш канал!", reply_markup=key_subscribe)


bot.polling()