import random, time

# Any time there is a random choice, put in an ai choice later

choicesdict = {"y": "told the dealer to pick it up", "n": "passed"}
suits = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}

suitColors = {"hearts": "red", "diamonds": "red", "clubs": "black", "spades": "black"}
nonTrumpRanks = ["A", "K", "Q", "J", "T", "9"]


class card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.isTrump = False
        self.displayValue = str(value) + str(suits[suit])
        self.color = suitColors[suit]


def deckCreator():
    deck = []
    for i in nonTrumpRanks:
        for x in suits:
            deck.append(card(i, x))
    return deck


totalCards = deckCreator()


class team(object):
    def __init__(self, name):
        #  self.teamPlayers = [teamMate1, teamMate2]
        self.name = name
        self.points = 0
        self.handScore = 0
        self.isWinningHand = False


class player(object):
    def __init__(self, name, playerTeam):
        self.cardsInHand = []
        self.displayHand = []
        self.name = name
        self.team = playerTeam

    def populateDisplayHand(self):
        for i in self.cardsInHand:
            self.displayHand.append(i.displayValue)

    def removeCard(self, cardToRemove):
        self.cardsInHand.remove(cardToRemove)
        self.displayHand.remove(cardToRemove.displayValue)

    def playCard(self, trump, followSuit, _leftBauer):
        playableCards = []
        for i in self.cardsInHand:
            if trump == followSuit:
                if i.suit == followSuit:
                    playableCards.append(i)
                if i == _leftBauer:
                    playableCards.append(i)
            elif i.suit == followSuit and i != _leftBauer:
                playableCards.append(i)
        if not playableCards:
            for i in self.cardsInHand:
                playableCards.append(i)
        if self.name == "user":
            print("\nYour cards:", self.displayHand, "\n")
            cardInput = input("which card would you like to discard?\n\n").upper()
            cardThrow = None
            for x in playableCards:
                # selects the card in your hand with a display value == cardThrow
                if x.displayValue == cardInput:
                    cardThrow = x
                    break
            if cardThrow is not None:
                # means that it was a legal play
                self.removeCard(cardThrow)
                print()
        else:
            # Put a choice in here at some point
            cardThrow = random.choice(playableCards)
            self.removeCard(cardThrow)
        if cardThrow is not None:
            return cardThrow
        else:
            return True

    def aiFakeDiscard(self, _trumpSuit):
        testHand = []
        for i in self.cardsInHand:
            testHand.append(i)
        for i in testHand:
            if i.suit == _trumpSuit:
                testHand.remove(i)
        if not testHand:
            self.cardsInHand.sort(key=lambda x: (nonTrumpRanks.index(x.value)), reverse=True)
            if self.cardsInHand[0].value != "J":
                self.removeCard(self.cardsInHand[0])
            elif self.cardsInHand[1].value != "J":
                self.removeCard(self.cardsInHand[1])
            else:
                self.removeCard(self.cardsInHand[2])
        else:
            testHand.sort(key=lambda x: (nonTrumpRanks.index(x.value)), reverse=True)
            self.removeCard(testHand[0])

    def aiPlayCard(self, cardsPlayed, _trumpSuit):
        # something goes here
        if cardsPlayed[0][1].team == self.team:
            # this will change
            self.aiFakeDiscard(_trumpSuit)
            return


userTeam = team("your team")
otherTeam = team("the other team")

teams = [userTeam, otherTeam]

user = player("user", userTeam)
crossPlayer = player("crossPlayer", userTeam)
leftPlayer = player("leftPlayer", otherTeam)
rightPlayer = player("rightPlayer", otherTeam)

clockwiseOrder = [user, leftPlayer, crossPlayer, rightPlayer, user, leftPlayer, crossPlayer, rightPlayer, user,
                  leftPlayer, crossPlayer, rightPlayer]


# this is so we can cycle through dealers and choosers, etc without index errors


def shuffleAndDeal(dealer):
    # also chooses the first dealer from the first black jack rule
    for i in range(4):
        clockwiseOrder[i].cardsInHand = []
        clockwiseOrder[i].displayHand = []
    random.shuffle(totalCards)
    shuffledDeck = totalCards
    dealFirst = clockwiseOrder.index(dealer) + 1
    cardsDelt = {
        0: [0, 1, 2, 10, 11],
        1: [3, 4, 12, 13, 14],
        2: [5, 6, 7, 15, 16],
        3: [8, 9, 17, 18, 19]
    }
    for i in cardsDelt:
        for x in range(5):
            clockwiseOrder[dealFirst + i].cardsInHand.append(shuffledDeck[cardsDelt[i][x]])
    for k in range(4):
        clockwiseOrder[k].populateDisplayHand()
    for n in shuffledDeck:
        if n.color == "black" and n.value == "J":
            blackJack = n
            break
    for l in cardsDelt:
        if shuffledDeck.index(blackJack) in cardsDelt[l]:
            firstDealer = clockwiseOrder[dealFirst + l]
    extras = shuffledDeck[20:23]
    if blackJack in extras:
        firstDealer = clockwiseOrder[dealFirst + extras.index(blackJack)]
    return extras, firstDealer


def cardRankCreator(trump, _color, followSuit):
    rankedCards = []
    guh = []
    for i in totalCards:
        if i.suit == trump and i.value == "J":
            rankedCards.append(i)
    for i in totalCards:
        if i.color == _color and i.value == "J" and i not in rankedCards:
            leftBauer = i
            rankedCards.append(i)
    for i in totalCards:
        if i.suit == trump and i.value != "J":
            guh.append(i)
    guh.sort(key=lambda x: (nonTrumpRanks.index(x.value)))
    for i in guh:
        rankedCards.append(i)
    guh = []
    if followSuit != trump:
        for i in totalCards:
            if i.suit == followSuit:
                guh.append(i)
        guh.sort(key=lambda x: (nonTrumpRanks.index(x.value)))
        for i in guh:
            rankedCards.append(i)
    for i in totalCards:
        if i not in rankedCards:
            rankedCards.append(i)
    for i in range(7):
        rankedCards[i].isTrump = True
    return rankedCards, leftBauer


def aiTrumpChooser(_chooser, dealer, cardUp):
    pickUpChance = 0
    if _chooser.team == dealer.team and cardUp.value == "J":
        pickUpChance += .75
    elif _chooser.team != dealer.team and cardUp.value == "J":
        pickUpChance -= .75
    sameSuitCards = 0
    noneOf = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}
    for i in _chooser.cardsInHand:
        noneOf.pop(i.suit, None)
        if i.color == cardUp.color and i.value == "J":
            pickUpChance += .625
        if i.suit == cardUp.suit:
            if i.value == "j":
                pickUpChance += .5
            sameSuitCards += 1
    if len(noneOf) != 0 and cardUp.suit not in noneOf.keys():
        pickUpChance += .75
    if cardUp.suit in noneOf.keys():
        pickUpChance -= 1
    if sameSuitCards >= 4:
        pickUpChance += 1
    elif sameSuitCards <= 1:
        pickUpChance -= .25
    elif (3 >= sameSuitCards >= 2) and _chooser.team == dealer.team:
        pickUpChance += .25
    return pickUpChance


def trumpChooser(dealer):
    # 115 lines of pure unreadable nonsense, but it works, so I'm not changing it.
    whoDidWhat = []
    kitty, doesntMattter = shuffleAndDeal(dealer)
    print("the dealer is", dealer.name)
    print("The card on the table is \n\n", kitty[0].displayValue, "\n")
    suitsLeft = list(suits.keys())
    suitsLeft.remove(kitty[0].suit)
    for i in range(1, 9):
        chooser = clockwiseOrder[clockwiseOrder.index(dealer) + i]
        if i > 4:
            if i == 5:
                whoDidWhat = []
                input("hit enter again to continue")
                print("\033[H\033[J")
                print("the card that was passed on was", kitty[0].displayValue)
                for x in range(9):
                    suitsLeft.append("pass")
            if i == 8:
                suitsLeft = list(filter(lambda a: a != "pass", suitsLeft))
            if chooser == user:
                while True:
                    print("Your cards", user.displayHand, "\n")
                    trumpInput = input("choose a suit or type 'pass'").lower()
                    if trumpInput in suitsLeft:
                        break
                    input("you have to type a real suit or pass\nRemember you cannot pick the wuit you previously passed on\n\n double remember that if you are the dealer you cannot type pass\n   hit enter to try again")
                    print("\033[H\033[J")
                    print("the card that was passed on was", kitty[0].displayValue, "\n\n")
                    for i in whoDidWhat:
                        if i != user:
                            print(i.name, "passed")
                        else:
                            break
                if trumpInput != "pass":
                    trumpChoice = trumpInput
                    whoCalled = chooser.team
                    break
            else:
                trumpChoice = random.choice(suitsLeft)
                if trumpChoice != "pass":
                    print("\n", chooser.name, "chose", trumpChoice, "as trump\n")
                    whoCalled = chooser.team
                    break
                else:
                    print(chooser.name, "passed")
                whoDidWhat.append(chooser)
        else:
            if chooser == user:
                while True:
                    print("\nYour cards", user.displayHand)
                    if user == dealer:
                        pickUp = input("\nWould you like to pick it up? Y/N\n").lower()
                    else:
                        pickUp = input("\nWould you like " + dealer.name + " to pick it up? Y/N\n")
                    if pickUp == "y" or pickUp == "n":
                        whoDidWhat.append([chooser, choicesdict[pickUp]])
                        print()
                        break
                    else:
                        input("please either type 'Y', 'N'\n    Hit enter to continue")
                        print("\033[H\033[J")
                        print("the dealer is", dealer.name)
                        print("The card on the table is \n\n", kitty[0].displayValue, "\n")
                        for j in whoDidWhat:
                            print(j[0].name, j[1])
                        continue
            else:
                aiChoice = aiTrumpChooser(chooser, dealer, kitty[0])
                # print(chooser.name, "cards:", chooser.displayHand)
                if aiChoice > 1:
                    pickUp = "y"
                    whoDidWhat.append([chooser, "told you to pick it up"])
                else:
                    pickUp = "n"
                    whoDidWhat.append([chooser, "passed"])
            if pickUp == "y":
                if user != chooser:
                    print(chooser.name, "told", dealer.name, "to pick it up")
                trumpChoice = kitty[0].suit
                while True:
                    if user == dealer:
                        four = user.playCard(None, None, None)
                        if four:
                            input("you must type a card that is in your hand\n   hit enter to try again")
                            print("\033[H\033[J")
                            print("the dealer is", dealer.name)
                            print("The card on the table is \n\n", kitty[0].displayValue, "\n")
                            for n in whoDidWhat:
                                print(n[0].name, n[1])
                                if n[1] != "passed":
                                    break
                            continue
                    else:
                        dealer.aiFakeDiscard(trumpChoice)
                    dealer.cardsInHand.append(kitty[0])
                    dealer.displayHand.append(kitty[0].displayValue)
                    whoCalled = chooser.team
                    break
                break
            elif pickUp == "n" and chooser != user:
                print(chooser.name, "passed")
    trumpChoiceColor = suitColors[trumpChoice]
    return trumpChoice, trumpChoiceColor, whoCalled


def playTrick(dealer, lastTrickWinner, _trumpSuit, _trumpColor):
    cardsPlayed = []
    test, leftBauer = cardRankCreator(_trumpSuit, _trumpColor, None)
    if dealer is None:
        firstPlayer = lastTrickWinner
    elif lastTrickWinner is None:
        firstPlayer = clockwiseOrder[clockwiseOrder.index(dealer) + 1]
    if firstPlayer == user:
        while True:
            print("the trump suit is", _trumpSuit, "\n")
            print("your team has", userTeam.handScore, "tricks")
            print("the other team has", otherTeam.handScore, "tricks\n")
            userCardThrow = user.playCard(_trumpSuit, None, leftBauer)
            if userCardThrow:
                input("you must type a card that is in your hand.\n   hit enter to try again")
                print("\033[H\033[J")
                continue
            else:
                firstCardThrow = userCardThrow
                break
    else:
        print("the trump suit is", _trumpSuit, "\n")
        print("your team has", userTeam.handScore, "tricks")
        print("the other team has", otherTeam.handScore, "tricks\n")
        firstCardThrow = firstPlayer.playCard(_trumpSuit, None, leftBauer)
    if firstCardThrow != leftBauer:
        suitToFollow = firstCardThrow.suit
    else:
        oppositeSuit = {"hearts": "diamonds", "diamonds": "hearts", "spades": "clubs", "clubs": "spades"}
        suitToFollow = oppositeSuit[firstCardThrow.suit]
    cardsPlayed.append([firstCardThrow, firstPlayer])
    print(firstPlayer.name, " played: ", firstCardThrow.displayValue)
    cardRank, null = cardRankCreator(_trumpSuit, _trumpColor, suitToFollow)
    for i in range(1, 4):
        nextPlayer = clockwiseOrder[clockwiseOrder.index(firstPlayer) + i]
        while True:
            nextPlayerCardThrow = nextPlayer.playCard(_trumpSuit, suitToFollow, leftBauer)
            if not nextPlayerCardThrow:
                break
            else:
                input("please type a card in your hand or follow suit\n   Hit enter to continue")
                print("\033[H\033[J")
                print("the trump suit is", _trumpSuit, "\n")
                print("your team has", userTeam.handScore, "tricks")
                print("the other team has", otherTeam.handScore, "tricks\n")
                for j in cardsPlayed:
                    if j[1] != user:
                        print(j[1].name, "played: ", j[0].displayValue)
                    else:
                        break
        cardsPlayed.append([nextPlayerCardThrow, nextPlayer])
        print(nextPlayer.name, "played: ", nextPlayerCardThrow.displayValue)
    cardsPlayed.sort(key=lambda buh: cardRank.index(buh[0]))
    print()
    # for i in cardsPlayed:
    # print(i[0].displayValue, i[1].name)
    trickWinner = cardsPlayed[0][1]
    print(trickWinner.name, "won this trick with", cardsPlayed[0][0].displayValue, ", they will go fist next hand\n")
    input("hit enter to continue")
    print("\033[H\033[J")
    return trickWinner


def playHand(dealer):
    trumpSuit, trumpColor, teamThatCalled = trumpChooser(dealer)
    print("the team that called is", teamThatCalled.name, "\n")
    input("hit enter to coninue")
    print("\033[H\033[J")
    lastWinner = None
    for i in range(5):
        if i == 0:
            lastWinner = playTrick(dealer, lastWinner, trumpSuit, trumpColor)
        elif i > 0:
            lastWinner = playTrick(None, lastWinner, trumpSuit, trumpColor)
        lastWinner.team.handScore += 1
    for i in teams:
        if i.handScore >= 3:
            print(i.name, "won this hand. the next dealer is", clockwiseOrder[clockwiseOrder.index(dealer) + 1].name)
            i.points += 1
            if i.handScore == 5:
                i.points += 1
            if i != teamThatCalled:
                i.points += 1
            # figure out going alone?
        i.handScore = 0
    print("your team has", userTeam.points, "points")
    print("the other team has", otherTeam.points, "points")
    input("hit Enter to continue")
    print("\033[H\033[J")
    newDealer = clockwiseOrder[clockwiseOrder.index(dealer) + 1]
    return newDealer


def playGame():
    for i in range(20):
        thisdoesntmatter, dealer = shuffleAndDeal(random.choice(clockwiseOrder))
        playHand(dealer)
        for x in teams:
            if x.points >= 5:
                print(x.name, "won, would you like to play again? Y/N")
                playAgain = input().lower()
                while True:
                    if playAgain == "y" or playAgain == "n":
                        break
                    print("please either type 'y' or 'n'")
                if playAgain == "y":
                    playGame()
                else:
                    quit()


playGame()
