import csv
import os
from keyboard import keys_admin,keys_menu

def get(game):
    players = []
    with open("resources/players.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0] == game:
                players.append(row[1])
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
    game = bot.send_message(message.chat.id, "game")
    bot.register_next_step_handler(game, add_name, bot)


def add_name(message, bot):
    name = bot.send_message(message.chat.id, "first_name")
    bot.register_next_step_handler(name, add_nick, bot, message.text)


def add_nick(message, bot, game):
    nick = bot.send_message(message.chat.id, "nick")
    bot.register_next_step_handler(nick, add_url, bot, game, message.text)


def add_url(message, bot, game, name):
    url = bot.send_message(message.chat.id, "url")
    bot.register_next_step_handler(url, add_player, bot, game, name, message.text)


def add_player(message, bot, game, name, nick):
    player = {'game': game, 'name': name, 'nick': nick, 'url': message.text}
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['game', 'name', 'nick', 'url'])
        writer.writerow(player)



def remove_player(message):
    nick = bot.send_message(message.chat.id, "nick")
    bot.register_next_step_handler(nick, players.remove, bot)


def remove(message, bot):
    with open('resources/players.csv', 'r') as infile, open('resources/players_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            if row[2] != message.text:
                writer.writerow(row)

    os.replace('resources/players_edit.csv', 'resources/players.csv')