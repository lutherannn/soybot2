import random
playerHand, bankerHand = [], []
playerTotal, bankerTotal = 0, 0
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]

def drawCard(uh, ut, d, amt):
    global playerTotal, bankerTotal
    for _ in range(amt):
        card = random.choice(d)
        uh.append(card)
        d.remove(card)
        if ut == "p":
            playerTotal += card
            if playerTotal > 9:
                playerTotal = abs(playerTotal - 10)
        else:
            bankerTotal += card
            if bankerTotal > 9:
                bankerTotal = abs(bankerTotal - 10)

def baccyGame():
    r = []
    
    drawCard(playerHand, "p", deck, 2)
    drawCard(bankerHand, "b", deck, 2)
    
    r.append(f"{", ".join([str(x) for x in playerHand])}")
    r.append(playerTotal)
    r.append(f"{", ".join([str(x) for x in bankerHand])}")
    r.append(bankerTotal)

    if playerTotal > 5 and playerTotal < 8:
        drawCard(playerHand, "p", deck, 1)
    
    if bankerTotal < 3:
        drawCard(bankerHand, "b", deck, 1)
    elif bankerTotal == 3 and playerHand[-1] != 8:
        drawCard(bankerHand, "b", deck, 1)
    elif bankerTotal == 4 and playerHand[-1] in [2, 3, 4, 5, 6, 7]:
        drawCard(bankerHand, "b", deck, 1)
    elif bankerTotal == 5 and playerHand[-1] in [4, 5, 6, 7]:
        drawCard(bankerHand, "b", deck, 1)
    elif bankerTotal == 6 and playerHand[-1] in [6, 7]:
        drawCard(bankerHand, "b", deck, 1)
    
    r.append(f"{", ".join([str(x) for x in playerHand])}")
    r.append(playerTotal)
    r.append(f"{", ".join([str(x) for x in bankerHand])}")
    r.append(bankerTotal)

    if playerTotal > bankerTotal:
        r.append("Player wins!")
    elif bankerTotal > playerTotal:
        r.append("Banker wins!")
    else:
        r.append("It's a tie!")
    return r