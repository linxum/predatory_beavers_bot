import csv

def get(game):
    players = []
    with open("resources/players.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == game:
                players.append(row[1])
    return players


def new_player(player):
    with open("resources/players.csv", "a", newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, ['game', 'first_name', 'last_name', 'url'])
        writer.writerow(player)
