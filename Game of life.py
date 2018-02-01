import random, time, replit

currentlyLivingCells = []


class cell(object):
    def __init__(self, xValue, yValue, living):
        self.living = living
        if self.living:
            self.display = "■"
        if not self.living:
            self.display = "□"
        self.xValue = xValue
        self.yValue = yValue
        self.neighbors = []
        self.livingAdjacent = 0

    def kill(self):
        for i in self.neighbors:
            i.livingAdjacent -= 1
        self.living = False
        self.display = "□"

    def revive(self):
        for i in self.neighbors:
            i.livingAdjacent += 1
        self.living = True
        self.display = "■"


class miniGrid(object):
    def __init__(self, height, width, bigGrid, xStart, yStart):
        self.board = []
        self.height = height
        self.width = width
        self.bigGrid = bigGrid
        self.xStart = xStart
        self.yStart = yStart
        for i in range(self.height):
            self.board.append([])
            for x in range(self.width):
                self.board[i].append(cell(xStart + x, yStart + i, self.bigGrid[yStart + i][xStart + x].living))


def creator(length, height):
    board = []
    for i in range(height):
        board.append([])
        for l in range(length):
            board[i].append(cell(l, i, False))
            if board[i][l].living:
                currentlyLivingCells.append(board[i][l])
    for y in range(height):
        for x in range(length):
            # each of these ifs are to check that it's not on the edge to prevent index errors
            if x != 0:
                # Left side
                board[y][x].neighbors.append(board[y][x - 1])
            if x != (length - 1):
                # right side
                board[y][x].neighbors.append(board[y][x + 1])
            if y != 0:
                # bottom
                board[y][x].neighbors.append(board[y - 1][x])
            if y != (height - 1):
                # top
                board[y][x].neighbors.append(board[y + 1][x])
            if x != 0 and y != 0:
                # bottom left
                board[y][x].neighbors.append(board[y - 1][x - 1])
            if x != (length - 1) and y != 0:
                # bottom right
                board[y][x].neighbors.append(board[y - 1][x + 1])
            if x != 0 and y != (height - 1):
                # top left
                board[y][x].neighbors.append(board[y + 1][x - 1])
            if x != (length - 1) and y != (height - 1):
                # top right
                board[y][x].neighbors.append(board[y + 1][x + 1])
    for y in board:
        for x in y:
            for n in x.neighbors:
                if n.living:
                    x.livingAdjacent += 1
    return board


def printer(gridInput, isTestGrid):
    if not isTestGrid:
        for i in gridInput:
            for x in i:
                print(x.display, end=" ")
            print()
    else:
        for i in gridInput.board:
            for x in i:
                print(x.display, end=" ")
            print()


def checker(tile, checkedTiles):
    if tile not in checkedTiles:
        if not tile.living and tile.livingAdjacent == 3:
            checkedTiles.append(tile)
            return "revive"
        elif tile.living and (tile.livingAdjacent > 3 or tile.livingAdjacent < 2):
            checkedTiles.append(tile)
            return "kill"


def generationStepper(gridInput):
    checkedCells = []
    reviveCells = []
    killCells = []
    for i in currentlyLivingCells:
        result = checker(i, checkedCells)
        if result == "revive":
            reviveCells.append(i)
        elif result == "kill":
            killCells.append(i)
        for n in i.neighbors:
            result2 = checker(n, checkedCells)
            if result2 == "revive":
                reviveCells.append(n)
            elif result2 == "kill":
                killCells.append(n)
    for i in reviveCells:
        gridInput[i.yValue][i.xValue].revive()
        currentlyLivingCells.append(gridInput[i.yValue][i.xValue])
    for i in killCells:
        gridInput[i.yValue][i.xValue].kill()
        currentlyLivingCells.remove(gridInput[i.yValue][i.xValue])


def pastGenerationsFiller(gridInput, miniHeight, miniWidth, gridHeightInput, gridWidthInput, generations):
    lineageList = []
    for i in range(generations):
        if i == 0:
            for x in range(gridWidthInput - miniWidth):
                for y in range(gridHeightInput - miniHeight):
                    lineageList.append([miniGrid(miniHeight, miniWidth, gridInput, x, y)])
        else:
            for n in range(gridWidthInput - miniWidth):
                for b in range(gridHeightInput - miniHeight):
                    lineageList[n * (gridHeightInput - miniHeight) + b].append(
                        miniGrid(miniHeight, miniWidth, gridInput, n, b))
        generationStepper(gridInput)
    return lineageList


def patternChecker(lineageList):
    for i in range(len(lineageList)):
        sameChecker = {}
        for x in range(len(lineageList[i])):
            if x != 0:
                for d in range(len(lineageList[i][x].board)):
                    for f in range(len(lineageList[i][x].board[d])):
                        sameChecker.update(
                            {lineageList[i][x].board[d][f].living: lineageList[i][x - 1].board[d][f].living})
                if sameChecker.keys() == sameChecker.values():
                    for n in lineageList[i]:
                        printer(n, True)
                        print()
                    return (lineageList[i])


gridHeight = 28
gridLength = 50

grid = creator(gridLength, gridHeight)

this = pastGenerationsFiller(grid, 3, 3, gridHeight, gridLength, 50)

patternChecker(this)
