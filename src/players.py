import csv


def get(game):
    players = []
    with open("resources/players.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == game:
                players.append(row[1])
    return players






def add_game(message, bot):
    game = bot.send_message(message.chat.id, "game")
    bot.register_next_step_handler(game, add_fname, bot)


def add_fname(message, bot):
    name = bot.send_message(message.chat.id, "first_name")
    bot.register_next_step_handler(name, add_lname, bot, message.text)


def add_lname(message, bot, game):
    name = bot.send_message(message.chat.id, "last_name")
    bot.register_next_step_handler(name, add_url, bot, game, message.text)


def add_url(message, bot, game, f_name):
    ur = bot.send_message(message.chat.id, "url")
    bot.register_next_step_handler(ur, add, game, f_name, message.text)


def add(message, bot, game = "", f_name = "", l_name = ""):
    player = {'game': game, 'first_name': f_name, 'last_name': l_name, 'url': message.text}
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['game', 'first_name', 'last_name', 'url'])
        writer.writerow(player)
    bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
    file.close()
