import csv
from telebot import types
import os
from keyboard import keys_admin, keys_menu, key_cancel


def get_name(text):
    first_space = text.find(" ")
    if first_space != -1:
        end_pos = text.find("\n", first_space)
        if end_pos != -1:
            name = text[first_space + 1:end_pos]
            return name
    return ""


def get(message, bot):
    count = 0
    with open('resources/resume.csv', "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            count += 1
            msg = "Имя: {name}\nИгра: {game}\nРанг: {rang}\nПочему?: {why}\nURL: {url}".format(name=row["name"],
                                                                                 game=row["game"],
                                                                                 rang=row['rang'],
                                                                                 why=row["why"],
                                                                                 url=row['url'])
            key_resume = types.InlineKeyboardMarkup()
            key_resume.add(types.InlineKeyboardButton(text="Y", callback_data="resume_yes"))
            key_resume.add(types.InlineKeyboardButton(text="N", callback_data="resume_no"))
            bot.send_message(message.chat.id, msg, reply_markup=key_resume)
        if count == 0:
            bot.send_message(message.chat.id, "Новых заявок нет")


def add_resume(message, bot):
    name = bot.send_message(message.chat.id, "Дорогой пользователь ❤️‍🔥\n\nМы постоянно находимся в поиске талантливых игроков среди студентов ВГУ. Если ты готов к соревнованиям и хочешь представить наш клуб в мире киберспорта, то скорее заполняй форму, проходи отбор и становись частью нашей команды!\n\nДля начала укажи своё полное ФИО, курс и факультет", reply_markup=key_cancel)
    bot.register_next_step_handler(name, add_game, bot)


def add_game(message, bot):
    game = bot.send_message(message.chat.id, "Укажи одну или несколько дисциплин, в которых ты выступаешь", reply_markup=key_cancel)
    bot.register_next_step_handler(game, add_rang, bot, message.text)


def add_rang(message, bot, name):
    rang = bot.send_message(message.chat.id, "Укажи свой игровой ранг, либо ссылку на игровой кабинет", reply_markup=key_cancel)
    bot.register_next_step_handler(rang, add_why, bot, name, message.text)

def add_why(message, bot, name, game):
    why = bot.send_message(message.chat.id, "Расскажи пару слов о себе и своём игровом опыте. Почему ты хочешь присоединиться к нам?", reply_markup=key_cancel)
    bot.register_next_step_handler(why, add_url, bot, name, game, message.text)


def add_url(message, bot, name, game, rang):
    url = bot.send_message(message.chat.id, "Укажи ссылку со своими контактами для обратной связи", reply_markup=key_cancel)
    bot.register_next_step_handler(url, add, bot, name, game, rang, message.text)


def add(message, bot, name, game, rang, why):
    resume = {'name': name, 'game': game, 'rang': rang, 'why': why, 'url': message.text}
    with open("resources/resume.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['name', 'game', 'rang', 'why', 'url'])
        writer.writerow(resume)
    bot.send_message(message.chat.id, "Твоя заявка уже отправлена администраторам ❤️‍🔥\n\nБлагодарим! Скоро с тобой свяжутся", reply_markup=keys_menu)


def remove(name):
    with open('resources/resume.csv', 'r', encoding='utf-8') as infile, open('resources/resume_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            if row[0] != name:
                writer.writerow(row)

    os.replace('resources/resume_edit.csv', 'resources/resume.csv')
