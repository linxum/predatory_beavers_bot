import telebot
from telebot import types
from subscribe import subscribe

token = "6578454575:AAE9ZgatzU730m4vslDHJqgQu8ayAYsHkDo"
channel_id = ""

bot = telebot.TeleBot(token)
keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Написать напутствие")


@bot.message_handler(commands=['start'])
def com_start(message):
    bot.reply_to(message, "Добро пожаловать в бот!", reply_markup=keys_menu)
    subscribe(message.chat.id)


# def send_message_on_subscribe(bot, channel_id, user_id):
#     if bot.get_chat_member(channel_id, user_id).status == "member":
#         bot.send_message(user_id, "Привет! Так как ты подписался на наш канал, то мы подумали, что ты бы хотел "
#                                   "попользоваться нашим ботом")


bot.polling()