import random
import modules.deck
from modules.wallets import Ledger


def returnWarGame(wager, player):
    ledger = Ledger()
    deck = modules.deck.returnNonSuitedDeck()
    card = random.choice(deck)
    playerCard = card
    deck.remove(card)
    card = random.choice(deck)
    dealerCard = card
    deck.remove(card)
    playerCardDisplay = ""
    dealerCardDisplay = ""

    if playerCard == 11:
        playerCardDisplay = "Jack"
    elif playerCard == 12:
        playerCardDisplay = "Queen"
    elif playerCard == 13:
        playerCardDisplay = "King"
    elif playerCard == 14:
        playerCardDisplay = "Ace"
    else:
        playerCardDisplay = playerCard

    if dealerCard == 11:
        dealerCardDisplay = "Jack"
    elif dealerCard == 12:
        dealerCardDisplay = "Queen"
    elif dealerCard == 13:
        dealerCardDisplay = "King"
    elif dealerCard == 14:
        dealerCardDisplay = "Ace"
    else:
        dealerCardDisplay = dealerCard

    if ledger.is_bet_high(player, wager):
        return f"Bet too high for your balance of: {ledger.find_wallet_by_authorid(player).balance}"
    else:
        ledger.update_balance_by_authorid(player, wager * -1)

    if playerCard > dealerCard:
        ledger.update_balance_by_authorid(player, wager * 2)
        return f"Player's {str(playerCardDisplay)} beats the dealer's {str(dealerCardDisplay)}"
    elif dealerCard > playerCard:
        return f"Dealer's {str(dealerCardDisplay)} beats the player's {str(playerCardDisplay)}"
    else:
        ledger.update_balance_by_authorid(player, wager)
        return f"The player and dealer both had {str(playerCardDisplay)}"
