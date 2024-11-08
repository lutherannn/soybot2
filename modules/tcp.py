import random
import collections
from modules.wallets import Ledger
import modules.deck

handRanks = {
    1: "High Card",
    2: "Pair",
    3: "Flush",
    4: "Straight",
    5: "Three of a Kind",
    6: "Straight Flush",
}


def dealStartingHands(usedDeck):
    h = []
    for _ in range(3):
        card = random.choice(usedDeck)
        h.append(card)
        usedDeck.remove(card)
    for _ in range(3):
        card = random.choice(usedDeck)
        h.append(card)
        usedDeck.remove(card)
    return h


def checkWinners(hand):
    r = []
    t = []
    for x in hand:
        if len(x) == 2:
            t.append(int(x[0]))
        else:
            t.append(int(x[0:2]))

    # high card
    r = [x for x in sorted(t)]
    r.append(1)

    # pair
    p = [item for item, count in collections.Counter(t).items() if count > 1]
    if len(p) == 1 and max(t) == p[0]:
        r = [[x for x in t if x not in p][0], p[0], 2]
    if len(p) == 1 and max(t) != p[0]:
        r = [[x for x in t if x not in p][0], p[0], 2]

    # flush
    if hand[0][-1] == hand[1][-1] and hand[0][-1] == hand[2][-1]:
        r = [x for x in sorted(t)]
        r.append(3)

    # straight
    st = sorted(t)
    if st[1] - st[0] == 1 and st[2] - st[0] == 2:
        r = [max(t), 4]

    # three of a kind
    if len(set(t)) == 1:
        r = [max(t), 5]

    # straight flush
    if r[-1] == 4 and hand[0][-1] == hand[1][-1] and hand[0][-1] == hand[2][-1]:
        r = [max(t), 6]

    return r


def findWinner(pw, dw):
    if pw[-1] > dw[-1]:
        return "Player wins"
    if dw[-1] > pw[-1]:
        return "Dealer wins"
    if pw[-1] == dw[-1]:
        # High card wins
        if pw[-1] == 1:
            if pw[2] > dw[2]:
                return "Player wins"
            if dw[2] > pw[2]:
                return "Dealer wins"
            if pw[2] == dw[2]:
                if pw[1] > dw[1]:
                    return "Player wins"
                if dw[1] > pw[1]:
                    return "Dealer wins"
                if pw[1] == dw[1]:
                    if pw[0] > dw[0]:
                        return "Player wins"
                    if dw[0] > pw[0]:
                        return "Dealer wins"
                    if pw[0] == dw[0]:
                        return "Player wins"
        # Pair wins
        if pw[-1] == 2 and dw[-1] == 2:
            if pw[1] > dw[1]:
                return "Player wins"
            if dw[1] > pw[1]:
                return "Dealer wins"
            else:
                if pw[0] > dw[0]:
                    return "Player wins"
                if dw[0] > pw[0]:
                    return "Dealer wins"
                else:
                    return "It's a tie"
        # Flush wins
        if pw[-1] == 3 and dw[-1] == 3:
            if pw[0] > dw[0]:
                return "Player wins"
            if dw[0] > pw[0]:
                return "Dealer wins"
            else:
                if pw[1] > dw[1]:
                    return "Player wins"
                if dw[1] > pw[1]:
                    return "Dealer wins"
                else:
                    if pw[2] > dw[1]:
                        return "Player wins"
                    if dw[2] > pw[2]:
                        return "Dealer wins"
                    else:
                        return "It's a tie"

        # Straight wins
        if pw[-1] == 4 and dw[-1] == 4:
            if pw[0] > dw[0]:
                return "Player wins"
            if dw[0] > pw[0]:
                return "Dealer wins"
            else:
                return "It's a tie"

        # Three of a kind wins
        if pw[-1] == 5 and dw[-1] == 5:
            if pw[0] > dw[0]:
                return "Player wins"
            if dw[0] > pw[0]:
                return "Dealer wins"
            else:
                return "It's a tie!"

        # Straight flush wins
        if pw[-1] == 6 and dw[-1] == 6:
            if pw[0] > dw[0]:
                return "Player wins"
            if dw[0] > pw[0]:
                return "Dealer wins"
            else:
                return "It's a tie"


def printHands(p, d):
    global playerHand, dealerHand
    ph = []
    dh = []
    for x in p:
        if len(x) > 2 and "10" not in x:
            if x[0:2] == "11":
                ph.append(f"J{x[-1]}")
            if x[0:2] == "12":
                ph.append(f"Q{x[-1]}")
            if x[0:2] == "13":
                ph.append(f"K{x[-1]}")
            if x[0:2] == "14":
                ph.append(f"A{x[-1]}")
        else:
            ph.append(x)
    for x in d:
        if len(x) > 2 and "10" not in x:
            if x[0:2] == "11":
                dh.append(f"J{x[-1]}")
            if x[0:2] == "12":
                dh.append(f"Q{x[-1]}")
            if x[0:2] == "13":
                dh.append(f"K{x[-1]}")
            if x[0:2] == "14":
                dh.append(f"A{x[-1]}")
        else:
            dh.append(x)
    return [", ".join(ph), ", ".join(dh)]


def returnHandType(wh):
    return f"{handRanks.get(int(wh[-1]))}"


def returnTcpGame(wager, player):
    ledger = Ledger()

    if ledger.is_bet_high(player, wager):
        return f"Bet too high for your balance of: {ledger.find_wallet_by_authorid(player).balance}"
    else:
        ledger.update_balance_by_authorid(player, wager * -1)
    tcpDeck = modules.deck.returnSuitedDeck()
    startingHands = dealStartingHands(tcpDeck)

    playerHand = startingHands[0:3]
    dealerHand = startingHands[3:]

    playerWins = checkWinners(playerHand)
    dealerWins = checkWinners(dealerHand)
    if "Player" in findWinner(playerWins, dealerWins):
        multipliers = {
            1: 2, 2: 2, 3: 4, 4: 7, 5: 31, 6: 41
        }
        win_amount = wager * multipliers.get(playerWins[-1], 1)
        ledger.update_balance_by_authorid(player, win_amount)
        return [printHands(playerHand, dealerHand)[0], printHands(playerHand, dealerHand)[1], findWinner(playerWins, dealerWins), returnHandType(playerWins)]
    else:
        return [printHands(playerHand, dealerHand)[0], printHands(playerHand, dealerHand)[1], findWinner(playerWins, dealerWins), returnHandType(dealerWins)]
