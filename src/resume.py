import csv
from telebot import types
import os


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
    with open('resources/resume.csv', "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            count += 1
            if row["checked"] == "False":
                msg = "Имя: {name}\nИгра: {game}\nПочему?: {why}".format(name=row["name"],
                                                                         game=row["game"],
                                                                         why=row["why"])
                key_resume = types.InlineKeyboardMarkup()
                key_resume.add(types.InlineKeyboardButton(text="Y", callback_data="resume_yes"))
                key_resume.add(types.InlineKeyboardButton(text="N", callback_data="resume_no"))
                bot.send_message(message.chat.id, msg, reply_markup=key_resume)
    if count == 0:
        bot.send_message(message.chat.id, "Новых заявок нет")


def check(name):
    with open("resources/resume.csv", "r") as fileR, open("resources/resume_edit.csv", "w", newline='\n') as fileW:
        reader = csv.reader(fileR)
        writer = csv.writer(fileW)
        writer.writerow(next(reader))
        for row in reader:
            if row[0] != name:
                writer.writerow(row)
            elif row[0] == name:
                row[3] = True
                writer.writerow(row)

    os.replace("resources/resume_edit.csv", "resources/resume.csv")


def remove(name):
    with open('resources/resume.csv', 'r') as infile, open('resources/resume_edit.csv', 'w+', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            if row[0] != name:
                writer.writerow(row)

    os.replace('resources/resume_edit.csv', 'resources/resume.csv')
