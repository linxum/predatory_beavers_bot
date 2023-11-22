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
import players
import resume

bot = telebot.TeleBot(tokens.tg_token())
channel_id = "@predatorybeaver"

keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Напутствие", "Оставить заявку")

keys_admin = types.ReplyKeyboardMarkup(True, True)
keys_admin.add("Получить заявки", "Изменить расписание", "Пожелания", "Изменить состав", "Отправить пост")

# hours_to_games = []

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

    post_text = vkParser.get_post_text(domain)
    pngs = vkParser.get_post_photos(domain)
    if len(pngs) == 1:
        photo = open(pngs[0], 'rb')
        bot.send_photo(message.chat.id, photo, caption=post_text)
        photo.close()
    elif len(pngs) > 1:
        bot.send_media_group(message.chat.id, [types.InputMediaPhoto(open(png, "rb"), caption=post_text) for png in pngs])
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
            schedule_games.get_message(bot, message)
        case "Напутствие":
            print(schedule_games.get_hours())
        case "Оставить заявку":
            resume.add_resume(message, bot)

        case "Изменить состав":
            if is_admin(channel_id, message.from_user.id):
                keys_player = types.ReplyKeyboardMarkup(True, True)
                keys_player.add("Добавить игрока", "Удалить игрока")
                bot.send_message(message.chat.id, "Выбери", reply_markup=keys_player)
        case "Добавить игрока":
            if is_admin(channel_id, message.from_user.id):
                players.add(message, bot)
                bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
        case "Удалить игрока":
            if is_admin(channel_id, message.from_user.id):
                players.remove_player(message)
                bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
        case "Изменить расписание":
            if is_admin(channel_id, message.from_user.id):
                keys_games = types.ReplyKeyboardMarkup(True, True)
                keys_games.add("Добавить матч", "Удалить матч")
                bot.send_message(message.chat.id, "Выбери", reply_markup=keys_games)
        case "Добавить матч":
            if is_admin(channel_id, message.from_user.id):
                schedule_games.add_enemy(message, bot)
                bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
        case "Удалить матч":
            if is_admin(channel_id, message.from_user.id):
                schedule_games.remove_games(message)
                bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
        case "Отправить пост":
            if is_admin(channel_id, message.from_user.id):
                newPost(message)
        case "Получить заявки":
            resume.get(message, bot)


def remove_games(message):
    enemy = bot.send_message(message.chat.id, "enemy")
    bot.register_next_step_handler(enemy, day)


def day(message):
    day = bot.send_message(message.chat.id, "day")
    bot.register_next_step_handler(day, schedule_games.remove, bot, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "resume_yes":
        resume.check(resume.get_name(call.message.text))
    elif call.data == "resume_no":
        resume.remove(resume.get_name(call.message.text))
    else:
        gamers = players.get(call.data)
        # TODO: строка вывода
        for gamer in gamers:
            bot.send_message(call.message.chat.id, gamer)


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


schedule.every().day.at("20:44:30").do(mailing.morning_notification, bot)
# for hour in hours_to_games:
#     schedule.every().day.at(hour.strftime('%H:%M')).do(mailing.morning_notification, bot)


class ScheduleMessage():

  def try_send_schedule():
    while True:
      schedule.run_pending()
      # hours_to_games = schedule_games.get_hours()
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
# bot.polling()
# TODO: возможность писать в боте напутствия для игроков, чтобы бот пересылал это сообщение в беседу с игроками
