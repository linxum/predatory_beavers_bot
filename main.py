import telebot
from telebot import types

token = "6578454575:AAE9ZgatzU730m4vslDHJqgQu8ayAYsHkDo"
channel_id = ""

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def com_start(message):
    bot.reply_to(message, "Добро пожаловать в бот!")


def send_message_on_subscribe(bot, channel_id, user_id):
    if bot.get_chat_member(channel_id, user_id).status == "member":
        bot.send_message(user_id, "Привет! Так как ты подписался на наш канал, то мы подумали, что ты бы хотел "
                                  "попользоваться нашим ботом")


bot.polling()