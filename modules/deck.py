def returnNonSuitedDeck():
    nonSuitedDeck = []
    for _ in range(4):
        for x in range(2, 15):
            nonSuitedDeck.append(x)
    return nonSuitedDeck


def returnSuitedDeck():
    suitedDeck = []
    suits = ["c", "h", "s", "d"]
    for x in range(2, 15):
        for y in suits:
            suitedDeck.append(f"{str(x)}{y}")
    return suitedDeck
