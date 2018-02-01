import enchant, re

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z"]
d = enchant.Dict("en_US")


def word_check(word1, word2):
    """Checks whether each word is real and whether they are the same length"""
    global startword
    global endword
    startwordcheck = re.fullmatch(r'[a-zA-Z]', word1)
    endwordcheck = re.fullmatch(r'[a-zA-Z]', word2)
    if startwordcheck is not None:
        print("start word not letters: error")
        startword = input("type a new starting word: ")
        word_check(startword, endword)
    if endwordcheck is not None:
        print("end word not letters: error")
        endword = input("type a new end word: ")
        word_check(startword, endword)
    startdictcheck = d.check(word1)
    enddictcheck = d.check(word2)
    if len(startword) != len(endword):
        print("word lengths do not match")
        startword = input("type a new starting word: ")
        endword = input("type a new end word: ")
        word_check(startword, endword)
    if not startdictcheck:
        print("start word not an english word: error")
        startword = input("type a new starting word: ")
        word_check(startword, endword)
    if not enddictcheck:
        print("end word not an english word: error")
        endword = input("type a new end word: ")
        word_check(startword, endword)


def findOneLetterAway(word):
    a = []
    splitword = list(word)
    for i in range(len(splitword)):
        for x in range(len(letters)):
            '''checks each possible combination of letters that are one letter
            away to see if they're real words. If they are, add them to the array,
            return the array'''
            splitword[i] = letters[x]
            testword = "".join(splitword)
            realword = d.check(testword)
            if realword == True and testword != word:
                a.append([testword])
                """returns nested list of each one letter away word,
                with each word as its own one element nested list.
                this is done so that we can append the score of the word to the nested"""
        splitword = list(word.lower())
    return a


def closenesscheck(start, test):
    startsplit = list(start[0])
    testsplit = list(test[0])
    '''splits start and test word into lists with each letter as an element.
    checks to see if the first letters are the same, the second letters are the same, etc...
    returns the number of letters that are the same letter in the same location in the word'''
    testscore = 0
    for i in range(len(startsplit)):
        if startsplit[i] == testsplit[i]:
            testscore += 1
    return (testscore)


def solve(b):
    wordlist = findOneLetterAway(b)
    """gets list of words one letter away from the curret word"""
    for i in range(len(wordlist)):
        score = closenesscheck(wordlist[i], [endword])
        wordlist[i].insert(0, score)
        """makes it so each element in wordlist is a nested list containing the actual word and the
        number of similar letters to the goal word."""
    wordlist.sort(reverse=True)
    # sort by which has the highest score
    # print(wordlist)
    if wordlist is None:
        path.remove(b)
        return None
        # if there are no possible words one letter away, return to the last iteration of the function
    for i in range(len(wordlist)):
        if wordlist[i][1] == endword:
            solvedpath.append(endword)
            return None
        if wordlist[i][1] in usedwords:
            if i == len(wordlist) - 1:
                return False
            continue
        else:
            path.append(wordlist[i][1])
            usedwords.append(wordlist[i][1])
            h = solve(wordlist[i][1])
            if not h:
                """if the word had already been used, the function returns false (line 87)
                when that happens, this if statement removes it from the current path and
                continues to the next element in wordlist."""
                path.remove(wordlist[i][1])
                continue
            if path:
                if wordlist[i][1] == path[-1]:
                    path.remove(wordlist[i][1])
                    solvedpath.append(wordlist[i][1])
                    """this case is only for when you have found the endword and are going back through
                    the function to print out the path it checks. the only case where the word being tested
                    is the last word in the path is if you have found the correct path to the endword.
                    this creates the solved path for you to print out in the end."""
                    return None


startword = input("type starting word: ").lower()
endword = input("type ending word: ").lower()
while True:
    usedwords = []
    path = []
    solvedpath = []
    word_check(startword.title(), endword.title())
    solve(startword)
    solvedpath.append(startword)
    solvedpath.reverse()
    print(solvedpath)
    print()
    startword = input("type starting word: ").lower()
    endword = input("type ending word: ").lower()
