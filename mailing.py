def subscribe(id):
    flag = False
    with open('id.txt', 'r+') as f:
        for line in f:
            if line == str(id) + '\n':
                flag = True

        if not flag:
            print(id, file=f)


def unsubscribe(id):
    with open("id.txt", "r") as f:
        lines = f.readlines()
    with open("id.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != str(id):
                f.write(line)