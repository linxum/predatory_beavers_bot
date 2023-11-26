import csv
from telebot import types
import os
from keyboard import keys_admin,keys_menu


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
            if row["checked"] == "False":
                count += 1
                msg = "Имя: {name}\nИгра: {game}\nПочему?: {why}\nURL: {url}".format(name=row["name"],
                                                                                     game=row["game"],
                                                                                     why=row["why"],
                                                                                     url=row['url'])
                key_resume = types.InlineKeyboardMarkup()
                key_resume.add(types.InlineKeyboardButton(text="Y", callback_data="resume_yes"))
                key_resume.add(types.InlineKeyboardButton(text="N", callback_data="resume_no"))
                bot.send_message(message.chat.id, msg, reply_markup=key_resume)
        if count == 0:
            bot.send_message(message.chat.id, "Новых заявок нет")


def check(name):
    with open("resources/resume.csv", "r", encoding='utf-8') as fileR, open("resources/resume_edit.csv", "w", newline='\n', encoding='utf-8') as fileW:
        reader = csv.reader(fileR)
        writer = csv.writer(fileW)
        writer.writerow(next(reader))
        for row in reader:
            if row[0] != name:
                writer.writerow(row)
            elif row[0] == name:
                row[5] = True
                writer.writerow(row)

    os.replace("resources/resume_edit.csv", "resources/resume.csv")


def add_resume(message, bot):
    name = bot.send_message(message.chat.id, "Имя?")
    bot.register_next_step_handler(name, add_game, bot)


def add_game(message, bot):
    game = bot.send_message(message.chat.id, "Игра?")
    bot.register_next_step_handler(game, add_why, bot, message.text)


def add_why(message, bot, name):
    why = bot.send_message(message.chat.id, "Почему?")
    bot.register_next_step_handler(why, add_url, bot, name, message.text)


def add_url(message, bot, name, game):
    url = bot.send_message(message.chat.id, "Ссылочку?")
    bot.register_next_step_handler(url, add, bot, name, game, message.text)


def add(message, bot, name, game, why):
    resume = {'name': name, 'game': game, 'why': why, 'url': message.text, 'checked': False}
    with open("resources/resume.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['name', 'game', 'why', 'url', 'checked'])
        writer.writerow(resume)
    bot.send_message(message.chat.id, "Успешно", reply_markup=keys_menu)


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
