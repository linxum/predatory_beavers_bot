import csv
import os
from keyboard import keys_admin, keys_menu, key_cancel

def get(game):
    players = []
    with open("resources/players.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['game'] == game:
                players.append(row)
    return players

def get_games():
    games = []
    with open("resources/players.csv", "r", encoding="utf-8") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            if not row['game'] in games:
                games.append(row['game'])
    return games

def add(message, bot):
    game = bot.send_message(message.chat.id, "Напиши дисциплину игрока", reply_markup=key_cancel)
    bot.register_next_step_handler(game, add_name, bot)


def add_name(message, bot):
    name = bot.send_message(message.chat.id, "Напиши ФИО игрока", reply_markup=key_cancel)
    bot.register_next_step_handler(name, add_url, bot, message.text)


def add_url(message, bot, game):
    url = bot.send_message(message.chat.id, "Напиши ссылку на соц. сеть", reply_markup=key_cancel)
    bot.register_next_step_handler(url, add_player, bot, game, message.text)


def add_player(message, bot, game, name):
    player = {'game': game, 'name': name, 'url': message.text}
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['name', 'game', 'url'])
        writer.writerow(player)
    bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)



def remove_player(message, bot):
    name = bot.send_message(message.chat.id, "Напиши ФИО игрока для удаления", reply_markup=key_cancel)
    bot.register_next_step_handler(name, remove, bot)


def remove(message, bot):
    check = False
    with open('resources/players.csv', 'r', encoding='utf-8') as infile, open('resources/players_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            if row[0] != message.text:
                writer.writerow(row)
            else:
                check = True

    os.replace('resources/players_edit.csv', 'resources/players.csv')
    if check:
        bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
    else:
        bot.send_message(message.chat.id, "Игрок не найден", reply_markup=keys_admin)