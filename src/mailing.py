import csv

def subscribe(id):
    flag = False
    with open('resources/ids.txt', 'r+') as f:
        for line in f:
            if line == str(id) + '\n':
                flag = True

        if not flag:
            print(id, file=f)