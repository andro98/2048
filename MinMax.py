from MyBoard import *
import math

# Score l kol node
nodescores=[0 for x in range (50000)]

# Child node le kol node fel tree
childlist = [[0 for x in range(0)] for y in range(50000)]

# Counter for actual node #
nodeNumber = 1

# Directions
directions = [100, 101, 102, 103]


def createMiniMaxTtree(depth):
    global nodescores
    global childlist
    global alphaBetaScore
    global nodeNumber
    nodescores = [0 for x in range(50000)]
    childlist = [[0 for x in range(0)] for y in range(50000)]
    nodeNumber = 1
    # passing first node, then current grid, root has no parent, depth as how much he will see
    # alpha with -ve infinity and beta with +ve infinity
    alphaBetaPruning(1, currentGrid, 0, depth, -math.inf, math.inf)


def alphaBetaPruning(node, grid, parent, depth, alpha, beta):
    global nodescores
    global childlist
    global nodeNumber

    # Like a base case when depth is 0 we need only next state
    if depth == 0:
        nodescores[node] = getScore(grid)
        return nodescores[node]

    # The turn of the player. making new node for every possible move
    if depth % 2 == 0:
        for i in range(4):
            nodeNumber += 1
            childlist[node].append(nodeNumber)
            if (movePossible(grid, directions[i])) == True:
                alpha = max(alpha,
                            alphaBetaPruning(nodeNumber, getNextGrid(grid, directions[i]), node, depth - 1, alpha, beta))
            if alpha >= beta:
                break
        nodescores[node] = alpha
        return alpha

    # The turn of the computer.looking through every possible outcome and picking up the worst ones
    else:
        zeros = []
        for i in range(16):
            if grid[i] == 0:
                zeros.append(i)

        gridTable = [[0 for x in range(16)] for y in range(0)]
        gridTableScores = []

        # Cases lel arkam ely momken ttl3ly fe dor el computer 2 we 4
        for i in zeros:
            grid[i] = 2
            gridTable.append(grid)
            grid[i] = 0

        for i in zeros:
            grid[i] = 4
            gridTable.append(grid)
            grid[i] = 0

        for i in gridTable:
            gridTableScores.append(getScore(i))

        for i in range(4):
            minimumScore = min(gridTableScores)
            indeks = gridTableScores.index(minimumScore)

            nodeNumber += 1
            childlist[node].append(nodeNumber)
            #if (grid != gridTable[indeks]):
            beta = min(beta, alphaBetaPruning(nodeNumber, gridTable[indeks], node, depth - 1, alpha, beta))

            if beta <= alpha:
                break

            gridTableScores[indeks] = math.inf

        nodescores[node] = beta
        return beta

# Returning the best move to perform
def getMoves():
    searchedValue = nodescores[1]

    for index, i in enumerate(childlist[1]):
        if nodescores[i] == searchedValue:
            return directions[index]
