import random, time, replit

gridHeight = 28
gridWidth = 50


# generally row == y and column == x

def neighborCoords(row, column, height, width):
    if row == 0 and column != 0 and column != width - 1:
        # top
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [0, 1] for columni in [-1, 0, 1] if
                     (rowi != 0 or columni != 0)]
    elif column == 0 and row != 0 and row != height - 1:
        # left
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0, 1] for columni in [0, 1] if
                     (rowi != 0 or columni != 0)]
    elif column == width - 1 and row != 0 and row != height - 1:
        # right
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0, 1] for columni in [-1, 0] if
                     (rowi != 0 or columni != 0)]
    elif row == height - 1 and column != 0 and column != width - 1:
        # bottom
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0] for columni in [-1, 0, 1] if
                     (rowi != 0 or columni != 0)]
    elif row == 0 and column == 0:
        # top left
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [0, 1] for columni in [0, 1] if
                     (rowi != 0 or columni != 0)]
    elif row == height - 1 and column == width - 1:
        # bottom right
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0] for columni in [-1, 0] if
                     (rowi != 0 or columni != 0)]
    elif row == 0 and column == width - 1:
        # top right
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [0, 1] for columni in [-1, 0] if
                     (rowi != 0 or columni != 0)]
    elif row == height - 1 and column == 0:
        # bottom left
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0] for columni in [0, 1] if
                     (rowi != 0 or columni != 0)]
    else:
        neighbors = [keyMaker(row + rowi, column + columni) for rowi in [-1, 0, 1] for columni in [-1, 0, 1] if
                     (rowi != 0 or columni != 0)]
    return neighbors


keyMaker = lambda row, column: "{},{}".format(row, column)
valueGetter = lambda row, column, grid: grid[keyMaker(row, column)]
scoreGetter = lambda row, column, height, width, grid: sum(
    valueGetter(int(i[0]), int(i[-1]), grid) for i in neighborCoords(row, column, height, width))
getLivingCells = lambda grid: [i for i in grid.keys() if grid.get(i) == 1]
getCellsToCheck = lambda height, width, grid: list(set(
    sum([neighborCoords(int(j[0]), int(j[-1]), height, width) for j in getLivingCells(grid)], getLivingCells(grid))))
firstBoard = lambda height, width: {keyMaker(row, column): 1 if random.random() > .5 else 0 for row in range(height) for
                                    column in range(width)}
cellNextGen = lambda row, column, height, width, lastBoard: 0 if (scoreGetter(row, column, height, width,
                                                                              lastBoard) < 2 or scoreGetter(row, column,
                                                                                                            height,
                                                                                                            width,
                                                                                                            lastBoard) > 3) and valueGetter(
    row, column, lastBoard) == 1 else 1 if scoreGetter(row, column, height, width, lastBoard) == 3 and valueGetter(row,
                                                                                                                   column,
                                                                                                                   lastBoard) == 0 else valueGetter(
    row, column, lastBoard)
nextBoard = lambda height, width, lastBoard: {
keyMaker(row, column): cellNextGen(row, column, height, width, lastBoard) if keyMaker(row, column) in getCellsToCheck(
    height, width, lastBoard) else valueGetter(row, column, lastBoard) for row in range(height) for column in
range(width)}
printableBoard = lambda height, width, grid: "\n".join(
    [" ".join(["■" if valueGetter(row, column, grid) == 1 else "□" for column in range(width)]) for row in
     range(height)])
g = firstBoard(gridHeight, gridWidth)


def cycler(height, width, first, generations):
    boards = [first]
    for f in range(generations):
        boards.append(nextBoard(height, width, boards[f]))
    return boards


lst = cycler(gridHeight, gridWidth, g, 150)

for i in lst:
    print(printableBoard(gridHeight, gridWidth, i), end="\n\n")
    time.sleep(.3)
    replit.clear()
