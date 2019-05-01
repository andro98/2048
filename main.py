from PIL import ImageGrab, ImageOps
import pyautogui

# Current Grid on Screen
currentGrid = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]

UP = 100
DOWN = 101
RIGHT = 102
LEFT = 103


# ALl the coordinates of the grid
class Cords:
    cord11 = (170, 270)
    cord12 = (270, 270)
    cord13 = (370, 270)
    cord14 = (470, 270)
    cord21 = (170, 370)
    cord22 = (270, 370)
    cord23 = (370, 370)
    cord24 = (470, 370)
    cord31 = (170, 480)
    cord32 = (270, 480)
    cord33 = (370, 480)
    cord34 = (470, 480)
    cord41 = (170, 590)
    cord42 = (270, 590)
    cord43 = (370, 590)
    cord44 = (470, 590)

    cordArray = [cord11, cord12, cord13, cord14,
                 cord21, cord22, cord23, cord24,
                 cord31, cord32, cord33, cord34,
                 cord41, cord42, cord43, cord44]


# ALL grayScale pixels to get known on tiles
class Values:
    empty = 195
    v_2 = 229
    v_4 = 225
    v_8 = 190
    v_16 = 172
    v_32 = 157
    v_64 = 135
    v_128 = 205
    v_256 = 201
    v_512 = 197
    v_1024 = 193
    v_2048 = 189

    valueArray = [empty, v_2, v_4, v_8, v_16, v_32, v_64
        , v_128, v_256, v_512, v_1024,
                  v_2048]


# Get image convert it to grayImage then to pixels for each cell
# and then check its values and save it in current grid
def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)

    for index, cord in enumerate(Cords.cordArray):
        pixel = grayImage.getpixel(cord)
        pos = Values.valueArray.index(pixel)
        if pos == 0:
            currentGrid[index] = 0
        else:
            currentGrid[index] = pow(2, pos)


def printGrid(grid):
    for i in range(16):
        if i % 4 == 0:
            print("[ " + str(grid[i]) + " " + str(grid[i + 1]) + " " + str(grid[i + 2]) + " " + str(grid[i + 3]) + " ]")

# Get a row and then move it left under game conditions
# getNextGrid method path the row based on the direction of play
# It is like a main one that work for 4 direction
def swipeRow(row):
    prev = -1
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:
        if element != 0:  # if the element not equal 0
            if prev == -1:
                prev = element
                temp[i] = element
                i += 1
            elif prev == element:
                temp[i - 1] = 2 * prev
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1
    return temp

# Get Current grid and move and return new grid
def getNextGrid(grid, move):
    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * j] = val
    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3 - j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3 - j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + (3 - j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + (3 - j)] = val

    return temp

def movePossible(grid,direction):
     if grid==getNextGrid(grid,direction):
         return false
     else:
         return true
#Give a Bonus to everyy emptycell
def EmptyTilesHer(grid):
     Zeros=0
     for  i in range(16):
         if grid[i]==0:
             Zeros+=1
     return Zeros
#hnrg3 23la value f grid
def maxValueHeuristic(grid):
    maximumValue = -1
    for i in range(16):
        maximumValue = max(maximumValue, grid[i])

    return maximumValue
#de 3shan 25li l ganb b3d m3ndhomsh diffrencegamed
def smoothnessHeuristic(grid):
    smoothness=0;
    for i in range(4):
        current=0
        while current<4 and grid[4*i+current]==0:
            current += 1
        if current >= 4:
            continue
        next=current+1
     while next<4:
         while next<4 and grid[i*4+next]==0:
             next+=1
         if next>=4:
             break
         currentValue = grid[i * 4 + current]
         nextValue = grid[i * 4 + next]
         smoothness -= abs(currentValue - nextValue)

         current = next
         next += 1
    for i in range(4):
        current=0
        while current<4 and grid[4*current+i]==0:
            current+=1
        if current>=4:
            continue
        next=current+1
        while next<4:
            while next<4 and grid[4*next+i]==0:
                next+=1
            if next>=4:
                break
            currentValue=grid[current*4+i]
            nextValue=grid[next*4+i]
            smoothness -= abs(currentValue - nextValue)

            current=next
            next+=1

    return smoothness
# Heurisitc giving bonus poitns for monotonic rows of tiles
def monotonicityHeurictic(grid):
    montonicityScore=[0,0,0,0]
    #left or right
    for i in range (4):
        current=0
        next=current+1
        while next<4 and grid[i*4+next]==0:
            next+=1
        if next>=4:
            next-=1
        currentValue = grid[i * 4 + current]
        nextValue = grid[i * 4 + next]
        if currentValue >nextValue:
            monotonicityScores[0] += nextValue - currentValue
        elif nextValue > currentValue:
            monotonicityScores[1] += currentValue - nextValue
        current = next
        next += 1

        # up/down direction
        for i in range(4):
            current = 0
            next = current + 4
            while next < 4:
                while next < 4 and grid[i + 4 * next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                currentValue = grid[i + 4 * current]
                nextValue = grid[i + 4 * next]

                if currentValue > nextValue:
                    monotonicityScores[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    monotonicityScores[3] += currentValue - nextValue
            current = next
            next += 1

        return 20 * max(monotonicityScores[0], monotonicityScores[1]) + max(monotonicityScores[2],
                                                                            monotonicityScores[3])
# give bonus in corners
def positionOfMaxValueHeuristic(grid):
    maxValue = maxValueHeuristic(grid)
    if maxValue == grid[0] or maxValue == grid[3] or maxValue == grid[12] or maxValue == grid[15]:
        return 5000
    else:
        return -5000
#weights for grid
def weightedTilesHeuristic(grid):
    scoreGrid = [4**15, 4**14, 4**13, 4**12,
                 4**8,  4**9,  4**10, 4**11,
                 4**7,  4**6,  4**5,  4**4,
                 4**0,  4**1,  4**2,  4**3]

    score = 0
    for i in range(16):
        score += grid[i] * scoreGrid[i]

    return score
#--------------------------------------------
#score l kol node
nodescores=[0 for x in range (50000)]


childlist=[[0 for x in range (0)]for y in range (50000)]

nodeNumber = 1
directions=[100,101,102,103]


def createMiniMaxT(depth):
    global nodescores
    global childlist
    global alphaBetaScore
    global nodeNumber
    nodeScores = [0 for x in range(50000)]
    childList = [[0 for x in range(0)] for y in range(50000)]
    nodeNumber = 1
    #alphaBetaPruning(1, currentGrid, 0, depth, -math.inf, math.inf)
#def alphaBetaPruning(node, grid, parent, depth, alpha, beta):

# print(swipeRow([2, 0, 2, 2]))
# getGrid()
# printGrid(currentGrid)
# print("-------------")
# printGrid(getNextGrid(currentGrid, UP))
