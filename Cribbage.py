import random
from itertools import cycle

values = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10}
suits = ["C", "D", "H", "S"]


class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
        self.display_value = rank + suit


deck = [Card(i, j) for i in list(values.keys()) for j in suits]


class Player(object):
    def __init__(self, display_name):
        self.display_name = display_name
        self.hand = None
        self.display_hand = None
        # definitely a better way to do this one but I'm lazy


user = Player("user")
computer = Player("computer")
players = [user, computer] * 5

# maybe there's a better way to go back and forth but we're leaving this for now.


def who_deals_first():
    user.first_choice = random.choice(deck)
    computer.first_choice = random.choice(deck)
    if user.first_choice == computer.first_choice:
        return who_deals_first()
        # if they pick the same card just choose again
    if user.first_choice.rank == computer.first_choice.rank:
        return max([user, computer], key=lambda x: suits.index(x.first_choice.suit))
    return max([user, computer], key=lambda x: x.first_choice.value)


def shuffle_and_deal(dealer):
    # does the card that's up after the cut need to be a global variable?
    # can I make it a return value?
    deal_first = players.index(dealer) + 1
    random.shuffle(deck)
    for i in range(2):
        players[deal_first + i].hand = [deck[j*2 + i] for j in range(6)]
        players[deal_first + i].display_hand = [j.display_value for j in players[deal_first + i].hand]
    extra_cards = deck[12:]
    # this: vv is the card up that is a part of both hands
    return random.choice(extra_cards)


def pegging(dealer):
    tot = 0
    goes_first = players.index(dealer) + 1




