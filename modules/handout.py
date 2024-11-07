def giveHandout(authorid):
    log = []
    with open("assets/balances.txt", "r") as f:
        bals = [x.strip().split(" ") for x in f.readlines()]
        for x in bals:
            if (x[0] == authorid):
                x[1] = str(int(x[1]) + 1000)
            log.append(x)

    with open("assets/balances.txt", "w") as f:
        for x in log:
            f.write(str(x[0]) + " " + str(x[1]) + "\n")
    return True
