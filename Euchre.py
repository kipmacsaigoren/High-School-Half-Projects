import random

# Any time there is a random choice, put in an ai choice later
# underscores before variables just to not confuse function inputs with global variables
# I know that's bad code but at some point it's really hard to think of a synonym for "card"

choices_dict = {"y": "told the dealer to pick it up", "n": "passed"}
suits = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}

suit_colors = {"hearts": "red", "diamonds": "red", "clubs": "black", "spades": "black"}
non_trump_ranks = ["A", "K", "Q", "J", "T", "9"]


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.is_trump = False
        self.display_value = str(value) + str(suits[suit])
        self.color = suit_colors[suit]


def deck_creator():
    deck = []
    for i in non_trump_ranks:
        for x in suits:
            deck.append(Card(i, x))
    return deck


total_cards = deck_creator()


class Team(object):
    def __init__(self, name):
        #  self.teamPlayers = [teamMate1, teamMate2]
        self.name = name
        self.points = 0
        self.handScore = 0
        self.isWinningHand = False


class Player(object):
    def __init__(self, name, player_team):
        self.cards_in_hand = []
        self.display_hand = []
        self.name = name
        self.team = player_team

    def populate_display_hand(self):
        for i in self.cards_in_hand:
            self.display_hand.append(i.displayValue)

    def remove_card(self, card_to_remove):
        self.cards_in_hand.remove(card_to_remove)
        self.display_hand.remove(card_to_remove.displayValue)

    def play_card(self, trump, suit_to_follow, _left_bauer):
        playable_cards = []
        for i in self.cards_in_hand:
            if trump == suit_to_follow:
                if i.suit == suit_to_follow:
                    playable_cards.append(i)
                if i == _left_bauer:
                    playable_cards.append(i)
            elif i.suit == suit_to_follow and i != _left_bauer:
                playable_cards.append(i)
        if not playable_cards:
            for i in self.cards_in_hand:
                playable_cards.append(i)
        if self.name == "user":
            print("\nYour cards:", self.display_hand, "\n")
            card_input = input("which Card would you like to discard?\n\n").upper()
            card_throw = None
            for x in playable_cards:
                # selects the Card in your hand with a display value == card_throw
                if x.displayValue == card_input:
                    card_throw = x
                    break
            if card_throw is not None:
                # means that it was a legal play
                self.remove_card(card_throw)
                print()
        else:
            # Put a choice in here at some point
            card_throw = random.choice(playable_cards)
            self.remove_card(card_throw)
        if card_throw is not None:
            return card_throw
        else:
            return True

    def ai_fake_discard(self, _trump_suit):
        test_hand = []
        for i in self.cards_in_hand:
            test_hand.append(i)
        for i in test_hand:
            if i.suit == _trump_suit:
                test_hand.remove(i)
        if not test_hand:
            self.cards_in_hand.sort(key=lambda x: (non_trump_ranks.index(x.value)), reverse=True)
            if self.cards_in_hand[0].value != "J":
                self.remove_card(self.cards_in_hand[0])
            elif self.cards_in_hand[1].value != "J":
                self.remove_card(self.cards_in_hand[1])
            else:
                self.remove_card(self.cards_in_hand[2])
        else:
            test_hand.sort(key=lambda x: (non_trump_ranks.index(x.value)), reverse=True)
            self.remove_card(test_hand[0])

    def ai_play_card(self, cards_played, _trump_suit):
        # something goes here
        if cards_played[0][1].team == self.team:
            # this will change
            self.ai_fake_discard(_trump_suit)
            return


userTeam = Team("your Team")
otherTeam = Team("the other Team")

teams = [userTeam, otherTeam]

user = Player("user", userTeam)
cross_player = Player("cross_player", userTeam)
left_player = Player("left_player", otherTeam)
right_player = Player("right_player", otherTeam)

clockwise_order = [user, left_player, cross_player, right_player, user, left_player, cross_player, right_player, user,
                   left_player, cross_player, right_player]


# this is so we can cycle through dealers and choosers, etc without index errors


def shuffle_and_deal(dealer):
    # also chooses the first dealer from the first black jack rule
    for i in range(4):
        clockwise_order[i].cards_in_hand = []
        clockwise_order[i].display_hand = []
    random.shuffle(total_cards)
    shuffled_deck = total_cards
    deal_first = clockwise_order.index(dealer) + 1
    cards_dealt = {
        0: [0, 1, 2, 10, 11],
        1: [3, 4, 12, 13, 14],
        2: [5, 6, 7, 15, 16],
        3: [8, 9, 17, 18, 19]
    }
    for i in cards_dealt:
        for x in range(5):
            clockwise_order[deal_first + i].cards_in_hand.append(shuffled_deck[cards_dealt[i][x]])
    for k in range(4):
        clockwise_order[k].populate_display_hand()
    for n in shuffled_deck:
        if n.color == "black" and n.value == "J":
            black_jack = n
            break
    for l in cards_dealt:
        if shuffled_deck.index(black_jack) in cards_dealt[l]:
            first_dealer = clockwise_order[deal_first + l]
    extras = shuffled_deck[20:23]
    if black_jack in extras:
        first_dealer = clockwise_order[deal_first + extras.index(black_jack)]
    return extras, first_dealer


def card_rank_creator(trump, _color, suit_to_follow):
    ranked_cards = []
    guh = []
    for i in total_cards:
        if i.suit == trump and i.value == "J":
            ranked_cards.append(i)
    for i in total_cards:
        if i.color == _color and i.value == "J" and i not in ranked_cards:
            left_bauer = i
            ranked_cards.append(i)
    for i in total_cards:
        if i.suit == trump and i.value != "J":
            guh.append(i)
    guh.sort(key=lambda x: (non_trump_ranks.index(x.value)))
    for i in guh:
        ranked_cards.append(i)
    guh = []
    if suit_to_follow != trump:
        for i in total_cards:
            if i.suit == suit_to_follow:
                guh.append(i)
        guh.sort(key=lambda x: (non_trump_ranks.index(x.value)))
        for i in guh:
            ranked_cards.append(i)
    for i in total_cards:
        if i not in ranked_cards:
            ranked_cards.append(i)
    for i in range(7):
        ranked_cards[i].is_trump = True
    return ranked_cards, left_bauer


def ai_trump_chooser(_chooser, dealer, card_up):
    pick_up_chance = 0
    if _chooser.team == dealer.team and card_up.value == "J":
        pick_up_chance += .75
    elif _chooser.team != dealer.team and card_up.value == "J":
        pick_up_chance -= .75
    same_suit_cards = 0
    none_of = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}
    for i in _chooser.cardsInHand:
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
    who_did_what = []
    kitty, doesnt_matter = shuffle_and_deal(dealer)
    print("the dealer is", dealer.name)
    print("The Card on the table is \n\n", kitty[0].display_value, "\n")
    suits_left = list(suits.keys())
    suits_left.remove(kitty[0].suit)
    for i in range(1, 9):
        chooser = clockwise_order[clockwise_order.index(dealer) + i]
        if i > 4:
            if i == 5:
                who_did_what = []
                input("hit enter again to continue")
                print("\033[H\033[J")
                print("the Card that was passed on was", kitty[0].display_value)
                for x in range(9):
                    suits_left.append("pass")
            if i == 8:
                suits_left = list(filter(lambda a: a != "pass", suits_left))
            if chooser == user:
                while True:
                    print("Your cards", user.display_hand, "\n")
                    trump_input = input("choose a suit or type 'pass'").lower()
                    if trump_input in suits_left:
                        break
                    input("you have to type a real suit or pass\n"
                          "Remember you cannot pick the suit you previously passed on\n\n "
                          "double remember that if you are the dealer you cannot type pass\n"
                          "    hit enter to try again")
                    print("\033[H\033[J")
                    print("the Card that was passed on was", kitty[0].display_value, "\n\n")
                    for j in who_did_what:
                        if j != user:
                            print(j.name, "passed")
                        else:
                            break
                if trump_input != "pass":
                    trump_choice = trump_input
                    who_called = chooser.team
                    break
            else:
                trump_choice = random.choice(suits_left)
                if trump_choice != "pass":
                    print("\n", chooser.name, "chose", trump_choice, "as trump\n")
                    who_called = chooser.team
                    break
                else:
                    print(chooser.name, "passed")
                who_did_what.append(chooser)
        else:
            if chooser == user:
                while True:
                    print("\nYour cards", user.display_hand)
                    if user == dealer:
                        pickup = input("\nWould you like to pick it up? Y/N\n").lower()
                    else:
                        pickup = input("\nWould you like " + dealer.name + " to pick it up? Y/N\n")
                    if pickup == "y" or pickup == "n":
                        who_did_what.append([chooser, choices_dict[pickup]])
                        print()
                        break
                    else:
                        input("please either type 'Y', 'N'\n    Hit enter to continue")
                        print("\033[H\033[J")
                        print("the dealer is", dealer.name)
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
                while True:
                    if user == dealer:
                        four = user.play_card(None, None, None)
                        if four:
                            input("you must type a Card that is in your hand\n   hit enter to try again")
                            print("\033[H\033[J")
                            print("the dealer is", dealer.name)
                            print("The Card on the table is \n\n", kitty[0].display_value, "\n")
                            for n in who_did_what:
                                print(n[0].name, n[1])
                                if n[1] != "passed":
                                    break
                            continue
                    else:
                        dealer.ai_fake_discard(trump_choice)
                    dealer.cardsInHand.append(kitty[0])
                    dealer.displayHand.append(kitty[0].display_value)
                    who_called = chooser.team
                    break
                break
            elif pickup == "n" and chooser != user:
                print(chooser.name, "passed")
    trump_choice_color = suit_colors[trump_choice]
    return trump_choice, trump_choice_color, who_called


def play_trick(dealer, last_trick_winner, _trump_suit, _trump_color):
    cards_played = []
    test, left_bauer = card_rank_creator(_trump_suit, _trump_color, None)
    if dealer is None:
        first_player = last_trick_winner
    elif last_trick_winner is None:
        first_player = clockwise_order[clockwise_order.index(dealer) + 1]
    if first_player == user:
        while True:
            print("the trump suit is", _trump_suit, "\n")
            print("your Team has", userTeam.handScore, "tricks")
            print("the other Team has", otherTeam.handScore, "tricks\n")
            user_card_throw = user.play_card(_trump_suit, None, left_bauer)
            if user_card_throw:
                input("you must type a Card that is in your hand.\n   hit enter to try again")
                print("\033[H\033[J")
                continue
            else:
                first_card_throw = user_card_throw
                break
    else:
        print("the trump suit is", _trump_suit, "\n")
        print("your Team has", userTeam.handScore, "tricks")
        print("the other Team has", otherTeam.handScore, "tricks\n")
        first_card_throw = first_player.play_card(_trump_suit, None, left_bauer)
    if first_card_throw != left_bauer:
        suit_to_follow = first_card_throw.suit
    else:
        opposite_suit = {"hearts": "diamonds", "diamonds": "hearts", "spades": "clubs", "clubs": "spades"}
        suit_to_follow = opposite_suit[first_card_throw.suit]
    cards_played.append([first_card_throw, first_player])
    print(first_player.name, " played: ", first_card_throw.displayValue)
    card_rank, null = card_rank_creator(_trump_suit, _trump_color, suit_to_follow)
    for i in range(1, 4):
        next_player = clockwise_order[clockwise_order.index(first_player) + i]
        while True:
            next_player_card_throw = next_player.play_card(_trump_suit, suit_to_follow, left_bauer)
            if not next_player_card_throw:
                break
            else:
                input("please type a Card in your hand or follow suit\n   Hit enter to continue")
                print("\033[H\033[J")
                print("the trump suit is", _trump_suit, "\n")
                print("your Team has", userTeam.handScore, "tricks")
                print("the other Team has", otherTeam.handScore, "tricks\n")
                for j in cards_played:
                    if j[1] != user:
                        print(j[1].name, "played: ", j[0].displayValue)
                    else:
                        break
        cards_played.append([next_player_card_throw, next_player])
        print(next_player.name, "played: ", next_player_card_throw.displayValue)
    cards_played.sort(key=lambda buh: card_rank.index(buh[0]))
    print()
    # for i in cardsPlayed:
    # print(i[0].display_value, i[1].name)
    trick_winner = cards_played[0][1]
    print(trick_winner.name, "won this trick with", cards_played[0][0].displayValue, ", they will go fist next hand\n")
    input("hit enter to continue")
    print("\033[H\033[J")
    return trick_winner


def play_hand(dealer):
    trump_suit, trump_color, team_that_called = trump_chooser(dealer)
    print("the Team that called is", team_that_called.name, "\n")
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
            print(i.name, "won this hand. the next dealer is", clockwise_order[clockwise_order.index(dealer) + 1].name)
            i.points += 1
            if i.handScore == 5:
                i.points += 1
            if i != team_that_called:
                i.points += 1
            # figure out going alone?
        i.handScore = 0
    print("your Team has", userTeam.points, "points")
    print("the other Team has", otherTeam.points, "points")
    input("hit Enter to continue")
    print("\033[H\033[J")
    new_dealer = clockwise_order[clockwise_order.index(dealer) + 1]
    return new_dealer


def play_game():
    for i in range(20):
        nothing, dealer = shuffle_and_deal(random.choice(clockwise_order))
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
