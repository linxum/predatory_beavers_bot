import telebot
from telebot import types
import mailing

token = "6578454575:AAE9ZgatzU730m4vslDHJqgQu8ayAYsHkDo"
bot = telebot.TeleBot(token)

keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Написать напутствие")


@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed("@predatorybeaver", message.from_user.id):
        key_subscribe = types.ReplyKeyboardMarkup(True, True)
        key_subscribe.add("Проверить подписку")

        get_link = types.InlineKeyboardMarkup()
        get_link.add(types.InlineKeyboardButton(text="PREDATORY BEAVERS", url="https://t.me/predatorybeaver"))

        bot.send_message(message.chat.id, "Ссылка на канал", reply_markup=get_link)
        bot.send_message(message.chat.id, "Для работы с ботом вам необходимо подписаться на наш канал!", reply_markup=key_subscribe)
    else:
        bot.send_message(message.chat.id, "Добро пожаловать в бот!", reply_markup=keys_menu)
        mailing.subscribe(message.chat.id)


def is_subscribed(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


@bot.message_handler(content_types=['text'])
def keys(message):
    match message.text:
        case "Проверить подписку":
            start(message)
        case "Состав":
            keys_games = types.InlineKeyboardMarkup()
            keys_games.add(types.InlineKeyboardButton(text="CS2", callback_data='cs2'))
            keys_games.add(types.InlineKeyboardButton(text="Dota 2", callback_data='dota'))
            bot.send_message(message.chat.id, "Выбери команду: ", reply_markup=keys_games)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    match call.data:
        case 'cs2':
            bot.send_message(call.message.chat.id, "CS2")
        case 'dota':
            bot.send_message(call.message.chat.id, "Dota")

bot.polling()
