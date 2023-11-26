import csv
from keyboard import keys_admin,keys_menu
import schedule_games


def subscribe(id):
    flag = False
    with open('resources/ids.txt', 'r+') as f:
        for line in f:
            if line == str(id) + '\n':
                flag = True

        if not flag:
            print(id, file=f)


def morning_notification(bot):
    if len(schedule_games.get_today_info()) > 0:
        for game in schedule_games.get_today_info():
            msg = "Сегодня в {hour}:{minute} состоится матч в игре {game} с командой {enemy}".format(hour=game['hour'],
                                                                                                 minute=game['minute'],
                                                                                                 game=game['game'],
                                                                                                 enemy=game['enemy'])
            for id in open('resources/ids.txt', 'r').readlines():
                bot.send_message(id, msg)