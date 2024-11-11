import random
from modules.wallets import Ledger

allNums = ["0", "00"]
for x in range(1, 37):
    allNums.append(str(x))

# Won't be implemented at the start, but just here for the future
firstTwelve = allNums[2:14]
secondTwelve = allNums[14:26]
thirdTwelve = allNums[26:]

redNums = ["1", "3", "5", "7", "9", "12", "14", "16", "18",
           "21", "23", "25", "27", "28", "30", "32", "34", "36"]
blackNums = [x for x in allNums[2:] if x not in redNums]

allWagers = ["red", "black", "odd", "even"]
for x in allNums:
    allWagers.append(x)


def getColor(num):
    if str(num) in redNums:
        return "red"
    elif str(num) in blackNums:
        return "black"
    else:
        return "green"


def isEven(num):
    if int(num) % 2 == 0:
        return True
    return False


def returnRouletteGame(wager, wagerAmt, player):
    wagerAmt = int(wagerAmt)
    ledger = Ledger()
    r = []
    if ledger.is_bet_high(player, wagerAmt):
        return [f"Bet too high for your balance of: {
            ledger.find_wallet_by_author_id(player).balance}"]
    number = random.choice(allNums)

    r.append(f"Number is: {number}, {getColor(number).capitalize()}")
    if wager not in allWagers:
        return ["Invalid wager, run command with no arguments for examples"]
    ledger.update_balance_by_authorid(player, wagerAmt * -1)
    if wager == "red" and getColor(number) == "red":
        ledger.update_balance_by_authorid(player, wagerAmt * 2)
        r.append(f"You win: {wagerAmt * 2}")
    elif wager == "black" and getColor(number) == "black":
        ledger.update_balance_by_authorid(player, wagerAmt * 2)
        r.append(f"You win: {wagerAmt * 2}")
    elif wager == "even" and isEven(number):
        ledger.update_balance_by_authorid(player, wagerAmt * 2)
        r.append(f"You win: {wagerAmt * 2}")
    elif wager == "odd" and not isEven(number):
        ledger.update_balance_by_authorid(player, wagerAmt * 2)
        r.append(f"You win: {wagerAmt * 2}")
    elif wager == number:
        ledger.update_balance_by_authorid(player, wagerAmt * 36)
        r.append(f"You win: {wagerAmt * 36}")
    else:
        r.append(f"You lose: {wagerAmt}")

    return r
