import random

values = ["A", "K", "Q", "J", "T", "9"]
suits = {"S": ["spades", "black"], "C": ["clubs", "black"], "D": ["diamonds", "red"], "H": ["hearts", "red"]}


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.color = suits[suit][1]
        self.is_trump = False
        # may or may not be necessary
        self.display_value = value + suit


deck = [Card(i, j) for i in values for j in list(suits.keys())]


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.display_hand = []
        self.team = None
        # definitely a better way to do this one but I'm lazy

    def remove_card(self, card_to_remove):
        self.display_hand.remove(card_to_remove.display_value)
        self.hand.remove(card_to_remove)

    def discard(self, display_message, reprint_message, legal_choice, conditions):
        # conditions should be a list of game conditions.
        # conditions is ordered as [suit to follow, trump suit, left_bauer, add more things as needed here]
        if self.name == "you":
            card_in_hand = True
            legal = True
            test_card = None
            while test_card is None:
                if card_in_hand is not True:
                    input("You must type a card that is in your hand\n     hit enter to continue")
                    print("\033[H\033[J")
                    print(reprint_message)
                elif not legal:
                    input(legal_choice.__doc__ + "\n      hit enter to continue")
                    print("\033[H\033[J")
                    print(reprint_message)
                    # should this be an input? (hit enter to continue?)
                    # probably dangerous to use the docstring as an error message but who cares really
                print("\nYour cards: ", self.display_hand, "\n")
                card_choice = input(display_message + " and hit enter\n")
                for x in self.hand:
                    if x.display_value == card_choice.upper():
                        # checks if the card is actually in the hand
                        # test_card will no longer be none breaking it out of the loop
                        test_card = x
                        break
                if test_card is None:
                    card_in_hand = False
                elif legal_choice(self, test_card, conditions) is False:
                    legal = False
                    test_card = None
                    # the card was in the hand but it was not a legal play so test_card has to be reset
            self.remove_card(test_card)
            return test_card
        else:
            # make it real sometime?
            while True:
                test_card = random.choice(self.hand)
                if legal_choice(self, test_card, conditions):
                    break
            self.remove_card(test_card)
            return test_card


class Team(object):
    def __init__(self, name, team_mate1, team_mate2):
        self.team_players = [team_mate1, team_mate2]
        for i in self.team_players:
            i.team = self
        self.name = name
        self.points = 0
        self.handScore = 0
        self.is_winning_hand = False


user = Player("you")
left_player = Player("Left Computer")
cross_player = Player("Cross Computer")
right_player = Player("Right Computer")
players = [user, left_player, cross_player, right_player] * 10

user_team = Team("your team", user, cross_player)
other_team = Team("the other team", left_player, right_player)

teams = [user_team, other_team]


def shuffle_and_deal(dealer):
    # also chooses the first dealer from the first black jack rule
    random.shuffle(deck)
    # and index for players, not a player object
    cards_dealt = {
        0: [0, 1, 2, 10, 11],
        1: [3, 4, 12, 13, 14],
        2: [5, 6, 7, 15, 16],
        3: [8, 9, 17, 18, 19]
    }
    extras = deck[20:23]
    for i in range(4):
        for x in range(5):
            players[players.index(dealer) + i].hand.append(deck[cards_dealt[i][x]])
            players[players.index(dealer) + i].display_hand.append(deck[cards_dealt[i][x]].display_value)
    return extras


def card_rank_creator(trump, color_inpt, suit_to_follow):
    # could definitely be more efficient, but not enough to notice or care for this
    ranked_cards = []
    pre_sorted = []
    # used to pre sort the non bauer cards before added into ranked cards
    for i in deck:
        if i.suit == trump and i.value == "J":
            # right bauer
            ranked_cards.append(i)
    for i in deck:
        if i.color == color_inpt and i.value == "J" and i not in ranked_cards:
            # left bauer
            left_bauer = i
            ranked_cards.append(i)
    for i in deck:
        if i.suit == trump and i.value != "J":
            # trump cards
            pre_sorted.append(i)
    pre_sorted.sort(key=lambda x: values.index(x.value))
    for i in pre_sorted:
        ranked_cards.append(i)
    pre_sorted = []
    if suit_to_follow != trump:
        for i in deck:
            if i.suit == suit_to_follow:
                # cards of the suit that was led
                pre_sorted.append(i)
        pre_sorted.sort(key=lambda x: values.index(x.value))
        for i in pre_sorted:
            ranked_cards.append(i)
    for i in deck:
        if i not in ranked_cards:
            # the rest of the cards. the order doesn't matter for these.
            ranked_cards.append(i)
    for i in range(7):
        ranked_cards[i].is_trump = True
        # necessary?
    return ranked_cards, left_bauer


def ai_trump_chooser(_chooser, dealer, card_up):
    pick_up_chance = 0
    if _chooser.team == dealer.team and card_up.value == "J":
        pick_up_chance += .75
    elif _chooser.team != dealer.team and card_up.value == "J":
        pick_up_chance -= .75
    same_suit_cards = 0
    none_of = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}
    for i in _chooser.hand:
        none_of.pop(i.suit, None)
        if i.color == card_up.color and i.value == "J":
            pick_up_chance += .625
        if i.suit == card_up.suit:
            if i.value == "j":
                pick_up_chance += .5
            same_suit_cards += 1
    if len(none_of) != 0 and card_up.suit not in none_of.keys():
        pick_up_chance += .75
    if card_up.suit in none_of.keys():
        pick_up_chance -= 1
    if same_suit_cards >= 4:
        pick_up_chance += 1
    elif same_suit_cards <= 1:
        pick_up_chance -= .25
    elif (3 >= same_suit_cards >= 2) and _chooser.team == dealer.team:
        pick_up_chance += .25
    return pick_up_chance


def trump_chooser(dealer):
    # 115 lines of pure unreadable nonsense, but it works, so I'm not changing it.
    # future kip is fixing it though
    choices_dict = {"y": "told the dealer to pick it up", "n": "passed"}
    who_did_what = []
    kitty = shuffle_and_deal(dealer)
    print("The dealer is", dealer.name, "(" + dealer.team.name + ")")
    print("The card on the table is \n\n", kitty[0].display_value, "\n")
    suits_left = [i[0] for i in suits.values()]
    suits_left.remove(suits[kitty[0].suit][0])
    for i in range(1, 9):
        chooser = players[players.index(dealer) + i]
        if i < 5:
            # we're in the process of choosing whether or not to pick up the kitty card
            # this part of the loop will run first (i<4)
            if chooser == user:
                while True:
                    print("\nYour cards", user.display_hand)
                    if user == dealer:
                        pickup = input("\nWould you like to pick it up? Y/N\n").lower()
                    else:
                        pickup = input("\nWould you like " + dealer.name + " to pick it up? Y/N\n")
                    if pickup == "y" or pickup == "n":
                        who_did_what.append([chooser, choices_dict[pickup]])
                        # so that we can reprint it
                        print()
                        break
                    else:
                        input("Please either type 'Y', 'N'\n    Hit enter to continue")
                        # clear the terminal
                        print("\033[H\033[J")
                        print("The dealer is " + dealer.name + " (" + dealer.team.name + ")")
                        print("The Card on the table is \n\n", kitty[0].display_value, "\n")
                        for j in who_did_what:
                            print(j[0].name, j[1])
                        continue
            else:
                ai_choice = ai_trump_chooser(chooser, dealer, kitty[0])
                # print(chooser.name, "cards:", chooser.display_hand)
                if ai_choice > 1:
                    pickup = "y"
                    who_did_what.append([chooser, "told you to pick it up"])
                else:
                    pickup = "n"
                    who_did_what.append([chooser, "passed"])
            if pickup == "y":
                if user != chooser:
                    print(chooser.name, "told", dealer.name, "to pick it up")
                trump_choice = kitty[0].suit
                thing_to_print = "The dealer is " + dealer.name + " (" + dealer.team.name + ")" + \
                                 "\nThe Card on the table is \n\n" + kitty[0].display_value + "\n" + \
                                 "\n".join([i[0].name + " " + i[1] for i in who_did_what]) + "\n"
                dealer.discard("Please select a card to discard", thing_to_print, lambda a, b, c: True, [None] * 10)
                # lambda: True should just return true. meaning any card is ok to choose
                dealer.hand.append(kitty[0])
                dealer.display_hand.append(kitty[0].display_value)
                who_called = chooser.team
                break
            elif pickup == "n" and chooser != user:
                print(chooser.name, "passed")
        else:
            if i == 5:
                who_did_what = []
                input("hit enter again to continue")
                for x in range(9):
                    # why is it added 9 times?
                    # is it more likely for the computer to choose pass?
                    suits_left.append("pass")
            elif i == 8:
                suits_left = list(filter(lambda a: a != "pass", suits_left))
            if chooser == user:
                while True:
                    print("\033[H\033[J")
                    print("the Card that was passed on was", kitty[0].display_value, "\n\n")
                    for j in who_did_what:
                        print(j[0], j[1])
                    print("\nYour cards:", user.display_hand, "\n")
                    trump_input = input("choose a suit as trump or type 'pass'").lower()
                    if trump_input in suits_left:
                        break
                    input("Please type a real suit or the word \"pass\"\n"
                          "Remember you cannot pick the suit that was previously passed on\n\n"
                          "If you are the dealer, you can't type pass\n"
                          "       hit enter to try again")
            else:
                trump_input = random.choice(suits_left)
            who_did_what.append([chooser.name, "passed"])
            if trump_input != "pass":
                who_called = chooser.team
                for j, k in suits.items():
                    if k[0] == trump_input:
                        trump_choice = j
                        break
                break
    trump_choice_color = suits[trump_choice][1]
    return trump_choice, trump_choice_color, who_called


def legal_play(player, card_input, conditions):
    """please follow suit if you can"""
    suit_to_follow = conditions[0]
    trump_suit = conditions[1]
    left_bauer = conditions[2]
    playable_cards = []
    for card in player.hand:
        if card.suit == suit_to_follow and card != left_bauer:
            playable_cards.append(card)
        if trump_suit == suit_to_follow:
            if card == left_bauer:
                playable_cards.append(card)
    if not playable_cards:
        playable_cards = player.hand
    if card_input in playable_cards:
        return True
    return False


def play_trick(dealer, last_trick_winner, trump_suit, trump_color):
    cards_played = []
    null, left_bauer = card_rank_creator(trump_suit, trump_color, None)
    # I just need the left bauer but can't get the ranked cards
    # This will do just that half of the function with none as an input for suit to follow
    discard_message = "The trump suit is " + suits[trump_suit][0] + \
                     "\n\nYour team has " + str(user_team.handScore) + " tricks" + \
                     "\nThe other Team has " + str(other_team.handScore) + " tricks\n"
    if dealer is None:
        first_player = last_trick_winner
    elif last_trick_winner is None:
        first_player = players[players.index(dealer) + 1]
    print(discard_message)
    first_card_throw = first_player.discard("please type a card to play from your hand", discard_message, lambda a, b, c: True, [None] * 10)
    if first_card_throw != left_bauer:
        suit_to_follow = first_card_throw.suit
    else:
        opposite_suit = {"H": "D", "D": "H", "S": "C", "C": "S"}
        suit_to_follow = opposite_suit[first_card_throw.suit]
    cards_played.append([first_card_throw, first_player])
    print(first_player.name, " played: ", first_card_throw.display_value)
    discard_message += str("\n\n" + first_player.name + " played: " + first_card_throw.display_value)
    card_rank, null = card_rank_creator(trump_suit, trump_color, suit_to_follow)
    for i in range(1, 4):
        next_player = players[players.index(first_player) + i]
        next_player_card_throw = next_player.discard("please type a card to play from your hand", discard_message, legal_play, [suit_to_follow, trump_suit, left_bauer])
        cards_played.append([next_player_card_throw, next_player])
        print(next_player.name, "played: ", next_player_card_throw.display_value)
        discard_message += str("\n" + next_player.name + "played: " + next_player_card_throw.display_value)
    cards_played.sort(key=lambda x: card_rank.index(x[0]))
    print()
    # for i in cardsPlayed:
    # print(i[0].display_value, i[1].name)
    trick_winner = cards_played[0][1]
    print(trick_winner.name, "won this trick with the", cards_played[0][0].display_value, ", and will go fist next hand\n")
    input("hit enter to continue")
    print("\033[H\033[J")
    return trick_winner


def play_hand(dealer):
    for i in players:
        i.hand = []
        i.display_hand = []
    trump_suit, trump_color, team_that_called = trump_chooser(dealer)
    print(team_that_called.name, "called", suits[trump_suit][0], "\n")
    input("hit enter to continue")
    print("\033[H\033[J")
    last_winner = None
    for i in range(5):
        if i == 0:
            last_winner = play_trick(dealer, last_winner, trump_suit, trump_color)
        elif i > 0:
            last_winner = play_trick(None, last_winner, trump_suit, trump_color)
        last_winner.team.handScore += 1
    for i in teams:
        if i.handScore >= 3:
            print(i.name, "won this hand. the next dealer is ", players[players.index(dealer) + 1].name, "(" + players[players.index(dealer) + 1].team.name + ")")
            # Im sorry about commas and +'s in the same statement. It's to get rid of the spaces with the  ('s
            i.points += 1
            if i.handScore == 5:
                i.points += 1
            if i != team_that_called:
                i.points += 1
            # figure out going alone?
        i.handScore = 0
    print("your Team has", user_team.points, "points")
    print("the other Team has", other_team.points, "points")
    input("hit Enter to continue")
    print("\033[H\033[J")
    new_dealer = players[players.index(dealer) + 1]
    return new_dealer


def play_game():
    for i in range(20):
        dealer = random.choice(players)
        play_hand(dealer)
        for x in teams:
            if x.points >= 5:
                print(x.name, "won, would you like to play again? Y/N")
                play_again = input().lower()
                while True:
                    if play_again == "y" or play_again == "n":
                        break
                    print("please either type 'y' or 'n'")
                if play_again == "y":
                    play_game()
                else:
                    quit()


play_game()

