import csv
import datetime
import os

from keyboard import keys_admin, key_cancel


def update_date():
    return datetime.datetime.now()


# def get_hours():
#     hours = []
#     with open('resources/games.csv', "r+") as f:
#         reader = csv.DictReader(f)
#         events = [datetime.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M') for row in reader]
#         for event in events:
#             if update_date().date() == event.date():
#                 hours.append(event - datetime.timedelta(hours=1))
#     return hours

def sort_csv(input_file = "resources/games.csv"):
    # Чтение CSV-файла
    with open(input_file, 'r', encoding='utf-8') as infile, open('resources/games_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        header = next(reader)  # Сохранение заголовка

        # Сортировка данных
        sorted_data = sorted(reader, key=lambda x: x[2])

    # Запись отсортированных данных в новый CSV-файл
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(sorted_data)
    os.replace('resources/games_edit.csv', 'resources/games.csv')


def get_message(bot, message):
    sort_csv()
    msg = "🔥 Расписание ближайших игр!\n"
    cur_game = ""
    with open("resources/games.csv", "r", encoding="utf-8") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            if row['game'] == cur_game:
                time = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M")
                msg += "- " + time.strftime("%d.%m в %H:%M") + f" против {row['enemy']}\n"
                if row['url'] != "-":
                    msg += f"Ссылка: {row['url']}\n"
            else:
                msg += f"\nВ дисциплине: {row['game']}\n"
                cur_game = row['game']
                time = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M")
                msg += "- " + time.strftime("%d.%m в %H:%M") + f" против {row['enemy']}\n"
                if row['url'] != "-":
                    msg += f"Ссылка: {row['url']}\n"
    bot.send_message(message.chat.id, msg)


def get_today_info():
    games = []
    with open("resources/games.csv", "r") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            time = datetime.datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M")
            if int(time.day) == update_date().day and int(time.month) == update_date().month and int(time.year) == update_date().year:
                games.append({'hour': time.hour, 'minute': time.minute, 'enemy': row['enemy'], 'game': row['game']})
    return games


def add_enemy(message, bot):
    enemy = bot.send_message(message.chat.id, "Напиши название команды противника", reply_markup=key_cancel)
    bot.register_next_step_handler(enemy, add_time, bot)


def add_time(message, bot):
    time = bot.send_message(message.chat.id, "Напиши время матча (формат: YYYY-MM-DD HH:MM)", reply_markup=key_cancel)
    bot.register_next_step_handler(time, add_game, bot, message.text)


def add_game(message, bot, enemy):
    game = bot.send_message(message.chat.id, "Напиши игру/дисциплину", reply_markup=key_cancel)
    bot.register_next_step_handler(game, add_url, bot, enemy, message.text)


def add_url(message, bot, enemy, time):
    url = bot.send_message(message.chat.id, "Напиши ссылку на матч", reply_markup=key_cancel)
    bot.register_next_step_handler(url, add, bot, enemy, time, message.text)


def add(message, bot, enemy, time, game):
    id = 0
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
    with open("resources/games.csv", "r") as fileR:
        reader = csv.DictReader(fileR)
        for row in reader:
            id += 1
        id += 1
    game = {'id': id, 'enemy': enemy, 'datetime': time.strftime("%Y-%m-%d %H:%M"), 'game': game, 'url': message.text}
    with open("resources/games.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['id', 'enemy', 'game', 'datetime', 'url'])
        writer.writerow(game)
    bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)


def auto_remove():
    with open('resources/games.csv', 'r', encoding='utf-8') as infile, open('resources/games_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Пропускаем заголовок
        header = next(reader)
        writer.writerow(header)
        day = update_date().day
        month = update_date().month
        year = update_date().year

        for row in reader:
            time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M")
            if time.day != day or time.month != month or time.year != year:
                row[3] = time.strftime("%Y-%m-%d %H:%M")
                writer.writerow(row)

    os.replace('resources/games_edit.csv', 'resources/games.csv')


def remove_games(message, bot):
    enemy = bot.send_message(message.chat.id, "Введите противника матча для удаления", reply_markup=key_cancel)
    bot.register_next_step_handler(enemy, day, bot)

def day(message, bot):
    day = bot.send_message(message.chat.id, "Введите день проведения матча", reply_markup=key_cancel)
    bot.register_next_step_handler(day, remove, bot, message.text)


def remove(message, bot, enemy):
    check = False
    with open('resources/games.csv', 'r', encoding='utf-8') as infile, open('resources/games_edit.csv', 'w+', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            date = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M")
            if row[1] != enemy and date.day != message.text:
                writer.writerow(row)
            else:
                check = True
    os.replace('resources/games_edit.csv', 'resources/games.csv')
    if check:
        bot.send_message(message.chat.id, "Успешно", reply_markup=keys_admin)
    else:
        bot.send_message(message.chat.id, "Матч не найден", reply_markup=keys_admin)
