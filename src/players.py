import csv


def get(game):
    players = []
    with open("resources/players.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == game:
                players.append(row[1])
    return players






def games(message, bot):
    game = bot.send_message(message.chat.id, "game")
    bot.register_next_step_handler(game, fame, bot)


def fame(message, bot):
    name = bot.send_message(message.chat.id, "first_name")
    bot.register_next_step_handler(name, lame, bot, message.text)


def lame(message, bot, game):
    name = bot.send_message(message.chat.id, "last_name")
    bot.register_next_step_handler(name, url, bot, game, message.text)


def url(message, bot, game, fames):
    ur = bot.send_message(message.chat.id, "url")
    bot.register_next_step_handler(ur, add_new, game, fames, message.text)


def add_new(message, game, fname, lname):
    player = {'game': game, 'first_name': fname, 'last_name': lname, 'url': message.text}
    new_player(player)


def new_player(player):
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['game', 'first_name', 'last_name', 'url'])
        writer.writerow(player)
