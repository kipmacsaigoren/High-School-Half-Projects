import enchant, re
from time import sleep
# enchant has apparently been dicontinued on 64 bit machines and so now only works on
# pythonanywhere.com
# 

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z"]
d = enchant.Dict("en_US")


def startGame(startWord, endWord, count):
    """Checks whether each word is real and whether they are the same length
    
    If someone keeps getting things wrong, suggessts two words or more tries"""
    sleep(0.75)
    # wait. just slow it down

    mistakesUntilSuggestion = 5 #??? is this reasonable?

    # assumes that eventually the person will give a correct set of words
    # otherwise i'll just never stop running. Whoops!
    if count > mistakesUntilSuggestion:
        
        print("\nTry going from 'bolt' to 'wrap' by hitting enter!\n")
        sleep(.4)
        moreTries = input("(hit any key then enter for more tries)")
        if moreTries != '':
            return startGame(startWord, endWord, 0)
        else:
            return 'bolt', 'wrap'

    if startWord == '' or endWord == '':
        print("\nempty string entered, please type something\n")
        startWord = input("type a new starting word:")
        endWord = input("type a new ending word:")
        count += 1
        return startGame(startWord, endWord, count)

    startLetterCheck = re.fullmatch(r'[a-zA-Z]', startWord)
    endLetterCheck = re.fullmatch(r'[a-zA-Z]', endWord)
    if startLetterCheck is not None:
        # word 1 has non-letter chars in it
        print("\nstart word not letters: error\n")
        startWord = input("type a new starting word: ")
        count += 1
        return startGame(startWord, endWord, count)
    if endLetterCheck is not None:
        # word 2 has non-letter chars in it
        print("\nend word not letters: error\n")
        endWord = input("type a new end word: ")
        count += 1
        return startGame(startWord, endWord, count)
    startdictcheck = d.check(startWord)
    enddictcheck = d.check(endWord)
    if len(startWord) != len(endWord):
        print("\nword lengths do not match\n")
        startWord = input("type a new starting word: ")
        endWord = input("type a new end word: ")
        count += 1
        return startGame(startWord, endWord, count)
    if not startdictcheck:
        print("\nstart word not an english word: error\n")
        startWord = input("type a new starting word: ")
        count += 1
        return startGame(startWord, endWord, count)
    if not enddictcheck:
        print("\nend word not an english word: error\n")
        endWord = input("type a new end word: ")
        count += 1
        return startGame(startWord, endWord, count)
    
    return startWord.lower(), endWord.lower()
    
    
    


def findOneLetterAway(inputWord, goal):
    oneAway = []
    splitword = list(inputWord.lower())
    for i in range(len(splitword)):
        for x in range(len(letters)):
            '''checks each possible combination of letters that are one letter
            away to see if they're real words. If they are, add them to the array,
            return the array. This is only really like 25^4 checks only 390k?
            The reason the variables are like that is because python
            is not c++ and it is very confusing to pass by reference or value.'''
            splitword[i] = letters[x]
            test = "".join(splitword)
            isReal = d.check(test)
            if isReal and test != inputWord:
                oneAway.append([closenesscheck(test, goal), test])
                """returns nested list of each one letter away word,
                with each word as its own one element nested list.
                this is done so that we can append the score of the word to the nested"""
        splitword = list(inputWord.lower())
        oneAway.sort(reverse=True)
        # sort by which is the closest to the goal word
    return oneAway


def closenesscheck(start, test):
    '''Given two words (strings) of the same length, returns how many letters are 
    identical and in the same position in the word'''
    return sum([1 for let in range(len(start)) if start[let] == test[let]])


def solve(currentPath, end, used):
    """takes in a list of words as the path, and end goal word and a list of used words
    checks to see if, using any of the next possible words in the ladder, there is a solution.

    if there is a solution, returns the solved path.
    otherwise it just returns None"""

    oneAway = findOneLetterAway(currentPath[-1], end)
    # gets list of words one letter away from the curret word

    # print(oneAway)
    if oneAway is None:
        return None
        # if there are no possible words one letter away, remove end of path
    for pair in range(len(oneAway)):
        if oneAway[pair][1] == end:
            # solved it!
            currentPath.append(end)
            return currentPath
        if oneAway[pair][1] in used:
            # already tried this one
            continue
        else:
            # this pair has a new word to try
            # print(currentPath, oneAway)
            currentPath.append(oneAway[pair][1])
            used.append(oneAway[pair][1])
            solution = solve(currentPath, end, used)
            if solution is None:
                # doesn't work, try the next one letter away
                continue
            else:
                return solution
    # we got to the end of the list of words one letter away. No solution.
    return None


def play():
    # Play the game! but how do I stop????
    startWord = input("type starting word: ").lower()
    endWord = input("type ending word: ").lower()
    while True:
        
        startWord, endWord = startGame(startWord.title(), endWord.title(), 0)

        if startWord == endWord:
            print([startWord], "good job, this was hard to calculate")
        else:
            solvedPath = solve([startWord], endWord, [])
            print(solvedPath)
        print()

        startWord = input("type starting word: ").lower()
        endWord = input("type ending word: ").lower()


play()

