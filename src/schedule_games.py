import csv


def get(bot, message):
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
