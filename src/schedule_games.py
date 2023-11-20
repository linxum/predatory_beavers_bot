import csv
import datetime
import os


def update_date():
    return datetime.datetime.now()

def get_message(bot, message):
    with open("resources/games.csv", "r") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            msg = "{day} {month} в {hour}:{minute} наша команда будет играть с {enemy} в {game}".format(day=row['day'],
                                                                                                        month=row['month'],
                                                                                                        hour=row['hour'],
                                                                                                        minute=row['minute'],
                                                                                                        enemy=row['enemy'],
                                                                                                        game=row['game'])
            bot.send_message(message.chat.id, msg)

def get_info():
    with open("resources/games.csv", "r") as fileR:
        reader = csv.DictReader(fileR)
        day = update_date().day
        month = update_date().month
        year = update_date().year
        for row in reader:
            if int(row['day']) == day and int(row['month']) == month and int(row['year']) == year:
                return {'hour': row['hour'], 'minute': row['minute'], 'enemy': row['enemy'], 'game': row['game']}


def add_enemy(message, bot):
    enemy = bot.send_message(message.chat.id, "enemy")
    bot.register_next_step_handler(enemy, add_day, bot)


def add_day(message, bot):
    day = bot.send_message(message.chat.id, "day")
    bot.register_next_step_handler(day, add_month, bot, message.text)


def add_month(message, bot, enemy):
    month = bot.send_message(message.chat.id, "month")
    bot.register_next_step_handler(month, add_year, bot, enemy, message.text)


def add_year(message, bot, enemy, day):
    year = bot.send_message(message.chat.id, "year")
    bot.register_next_step_handler(year, add_game, bot, enemy, day, message.text)


def add_game(message, bot, enemy, day, month):
    game = bot.send_message(message.chat.id, "game")
    bot.register_next_step_handler(game, add_hour, bot, enemy, day, month, message.text)


def add_hour(message, bot, enemy, day, month, year):
    hour = bot.send_message(message.chat.id, "hour")
    bot.register_next_step_handler(hour, add_minute, bot, enemy, day, month, year, message.text)


def add_minute(message, bot, enemy, day, month, year, game):
    minute = bot.send_message(message.chat.id, "minute")
    bot.register_next_step_handler(minute, add_url, bot, enemy, day, month, year, game, message.text)


def add_url(message, bot, enemy, day, month, year, game, hour):
    url = bot.send_message(message.chat.id, "url")
    bot.register_next_step_handler(url, add, bot, enemy, day, month, year, game, hour, message.text)


def add(message, bot, enemy, day, month, year, game, hour, minute):
    id = 0
    with open("resources/games.csv", "r") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            id += 1
        id += 1
    game = {'id': id, 'enemy': enemy, 'day': int(day), 'month': int(month), 'year': int(year), 'game': game, 'hour': int(hour), 'minute': int(minute), 'url': message.text}
    with open("resources/games.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['id', 'enemy', 'day', 'month', 'year', 'game', 'hour', 'minute', 'url'])
        writer.writerow(game)
    bot.send_message(message.chat.id, "Успешно")
    file.close()

def auto_remove():
    with open('resources/games.csv', 'r') as infile, open('resources/games_edit.csv', 'w+', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Пропускаем заголовок
        header = next(reader)
        writer.writerow(header)
        day = update_date().day
        month = update_date().month
        year = update_date().year
        # Удаляем строки, где значение 3-го столбца равно "nick"
        for row in reader:
            if int(row[2]) != day or int(row[3]) != month or int(row[4]) != year:
                writer.writerow(row)

    os.replace('resources/games_edit.csv', 'resources/games.csv')

def remove(message, bot, enemy):
    with open('resources/games.csv', 'r') as infile, open('resources/games_edit.csv', 'w+', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            if row[1] != enemy and row[2] != message.text:
                writer.writerow(row)

    os.replace('resources/games_edit.csv', 'resources/games.csv')
    bot.send_message(message.chat.id, "Успешно")