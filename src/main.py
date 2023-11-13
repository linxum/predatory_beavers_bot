import csv

import telebot
from telebot import types
import schedule
import time
from multiprocessing.context import Process

import mailing
import tokens
import vkParser
import schedule_games

bot = telebot.TeleBot(tokens.tg_token())
channel_id = "@predatorybeaver"

keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Напутствие", "Оставить заявку")

keys_admin = types.ReplyKeyboardMarkup(True, True)
keys_admin.add("Получить заявки", "Добавить матч", "Пожелания", "Изменить состав", "Добавить матч")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_admin(channel_id, message.from_user.id):
        if not is_subscribed(channel_id, message.from_user.id):
            key_subscribe = types.ReplyKeyboardMarkup(True, True)
            key_subscribe.add("Проверить подписку")

            get_link = types.InlineKeyboardMarkup()
            get_link.add(types.InlineKeyboardButton(text="PREDATORY BEAVERS", url="https://t.me/predatorybeaver"))

            bot.send_message(message.chat.id, "Ссылка на канал", reply_markup=get_link)
            bot.send_message(message.chat.id, "Для работы с ботом вам необходимо подписаться на наш канал!", reply_markup=key_subscribe)
        else:
            bot.send_message(message.chat.id, "Добро пожаловать в бот!", reply_markup=keys_menu)
            mailing.subscribe(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Привет, админ", reply_markup=keys_admin)


@bot.message_handler(commands=['post'])
def newPost(message):
    domain = "beavers_esports"

    # текст
    post_text = vkParser.get_post_text(domain)
    if post_text != "":
        bot.send_message(message.chat.id, post_text)

    # фото
    pngs = vkParser.get_post_photos(domain)
    if len(pngs) == 1:
        photo = open(pngs[0], 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
    elif len(pngs) > 1:
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(open(png, "rb")) for png in pngs])
    vkParser.delete_files(pngs)

    # видео
    urls_video = vkParser.get_post_video(domain)
    if len(urls_video) > 0:
        for url in urls_video:
            bot.send_message(message.chat.id, url)


def is_subscribed(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


def is_admin(chat_id, user_id):
    chat_member = bot.get_chat_member(channel_id, user_id)
    return chat_member.status in ['creator', 'administrator']


@bot.message_handler(content_types=['text'])
def keys(message):
    match message.text:
        case "Проверить подписку":
            start(message)
        case "Состав":
            keys_games = types.InlineKeyboardMarkup()
            keys_games.add(types.InlineKeyboardButton(text="CS2", callback_data='cs2'))
            keys_games.add(types.InlineKeyboardButton(text="Dota 2", callback_data='dota2'))
            bot.send_message(message.chat.id, "Выбери команду: ", reply_markup=keys_games)
        case "Расписание":
            schedule.get(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    match call.data:
        case 'cs2':
            with open("resources\players.csv", newline='', encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    if row[0] == 'cs2':
                        bot.send_message(call.message.chat.id, row[1])
        case 'dota2':
            with open("resources\players.csv", newline='', encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    if row[0] == 'dota2':
                        bot.send_message(call.message.chat.id, row[1])


# schedule.every().day.at("06:00").do(mail)


class ScheduleMessage():

  def try_send_schedule():
    while True:
      schedule.run_pending()
      time.sleep(1)

  def start_process():
    p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
    p1.start()


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        # keep_alive()
        bot.polling(none_stop=True)
    except:
        pass

# TODO: сделать два разных main для user и admin

# TODO: возможность оставить заявку на вступление в команду (либо просто написать сообщение и чтобы оно отправилось
#  администраторам, либо прям заполнение анкеты как в дайвинчике, там узнать дисциплину, ранг, опыт, пару слов о себе)
#
# TODO: возможность писать в боте напутствия для игроков, чтобы бот пересылал это сообщение в беседу с игроками
#
# TODO: парсинг счета матча с фейсита(ну это в самую последнюю очередь, вдруг получится)
