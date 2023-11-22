import csv
import os

def get(game):
    players = []
    with open("resources/players.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[0] == game:
                players.append(row[1])
    return players


def add(message, bot):
    game = bot.send_message(message.chat.id, "game")
    bot.register_next_step_handler(game, add_fname, bot)


def add_fname(message, bot):
    name = bot.send_message(message.chat.id, "first_name")
    bot.register_next_step_handler(name, add_nick, bot, message.text)


def add_nick(message, bot, game):
    nick = bot.send_message(message.chat.id, "nick")
    bot.register_next_step_handler(nick, add_lname, bot, game, message.text)


def add_lname(message, bot, game, f_name):
    name = bot.send_message(message.chat.id, "last_name")
    bot.register_next_step_handler(name, add_url, bot, game, f_name, message.text)


def add_url(message, bot, game, f_name, nick):
    url = bot.send_message(message.chat.id, "url")
    bot.register_next_step_handler(url, add_player, bot, game, f_name, nick, message.text)


def add_player(message, bot, game, f_name, nick, l_name):
    player = {'game': game, 'first_name': f_name, 'nick': nick, 'last_name': l_name, 'url': message.text}
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['game', 'first_name', 'nick', 'last_name', 'url'])
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