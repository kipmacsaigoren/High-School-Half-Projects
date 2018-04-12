import random

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
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.display_hand = None
        self.peg_hand = None
        self.peg_display = None
        # definitely a better way to do this one but I'm lazy

    def remove_card(self, card_to_remove):
        self.display_hand.remove(card_to_remove.display_value)
        self.hand.remove(card_to_remove)

    def discard(self, display_message, reprint):
        if self.name == "user":
            first_go = True
            test = None
            while test is None:
                # clear terminal here, reprint whatever at top
                if not first_go:
                    print("you must type a card that is in your hand\n")
                print("Your cards:\n", self.display_hand, "\n")
                card_choice = input(display_message + "\nand hit enter").upper()
                for x in self.hand:
                    if x.display_value == card_choice:
                        # checks if the card is actually in the hand
                        # test will no longer be none breaking it out of the loop
                        test = x
                        self.remove_card(x)
                        break
                if test is None:
                    first_go = False
            return test
        else:
            # make it real sometime?
            test = random.choice(self.hand)
            self.remove_card(test)
            return test


user = Player("user")
computer = Player("computer")
players = [user, computer] * 5

# maybe there's a better way to go back and forth but we're leaving this for now.
# something about cycles


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
    # what about the crib?
    # can I make them a return value?
    deal_first = players.index(dealer) + 1
    random.shuffle(deck)
    crib = []
    for i in range(2):
        current_player = players[deal_first + i]
        current_player.hand = [deck[j*2 + i] for j in range(6)]
        current_player.display_hand = [j.display_value for j in current_player.hand]
        for k in range(2):
            # select the cards to put in the crib
            crib.append(current_player.discard("please select card #{} to put into {}'s crib".format(k+1, dealer.name), None))
            # no reprint message, FOR NOW!
            # actually come to think of it there might not ever be one for selecting the crib
            # maybe reprint the card that was chosen?
    extra_cards = deck[12:]
    # this is the card up that is a part of both hands
    return random.choice(extra_cards), crib


shuffle_and_deal(user)
print(user.display_hand)






