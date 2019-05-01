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


# Check if next move is possible
# To avoide infinite loop
def movePossible(grid, direction):
    if grid == getNextGrid(grid, direction):
        return False
    else:
        return True

# Giving a direction it perform the move on keyboard
def performMove(move):
    if move == UP:
        print("UP")
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    if move == DOWN:
        print("DOWN")
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    if move == LEFT:
        print("LEFT")
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    if move == RIGHT:
        print("RIGHT")
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')

# Give score fo every empty tiles on board
def emptyScoreHer(grid):
    empty = 0
    for i in range(16):
        if grid[i] == 0:
            empty += 1

    return empty

# Get maximum number on board
def maxNumHer(grid):
    maxNum = -1
    for i in range(16):
        maxNum = max(maxNum, grid[i])

    return maxNum

# Heuristic using weighted grid to determine how many bonus points we are supposed to give
def weightedTilesHeuristic(grid):
    scoreGrid = [4**15, 4**14, 4**13, 4**12,
                 4**8,  4**9,  4**10, 4**11,
                 4**7,  4**6,  4**5,  4**4,
                 4**0,  4**1,  4**2,  4**3]

    score = 0
    for i in range(16):
        score += grid[i] * scoreGrid[i]

    return score

def smoothnessHeuristic(grid):
    smoothness = 0
    for i in range(4):
        current = 0
        while current < 4 and grid[4*i + current] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1
            if next >= 4:
                break

            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    for i in range(4):
        current = 0
        while current < 4 and grid[current*4 + i] == 0:
            current += 1
        if current >= 4:
            continue

        next = current + 1
        while next < 4:
            while next < 4 and grid[4*next + i]:
                next += 1
            if next >= 4:
                break

            currentValue = grid[current*4 + i]
            nextValue = grid[next*4 + i]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    return smoothness*10

# Heuristic giving bonus points for placing tile with maximum value at the corner of the board
def positionOfMaxValueHeuristic(grid):
    maxValue = maxNumHer(grid)
    if maxValue == grid[0] or maxValue == grid[3] or maxValue == grid[12] or maxValue == grid[15]:
        return 5000
    else:
        return -5000

# Function returning score of the given graph
# Feel free to modify it and play with the constants :)
def getScore(grid):
    emptyTilesScore = emptyScoreHer(grid) * 100
    maxValueScore = maxNumHer(grid) * 4
    weightedTilesScore = weightedTilesHeuristic(grid)

    positionOfMaxValueScore = positionOfMaxValueHeuristic(grid) * 5
    smoothnessScore = smoothnessHeuristic(grid) * 10
    # Exemplary score, try to modify it along with constants above
    # Little change can make huge difference
    return weightedTilesScore + maxValueScore + emptyTilesScore + smoothnessScore + positionOfMaxValueScore


# print(swipeRow([2, 0, 2, 2]))
# getGrid()
# printGrid(currentGrid)
# print("-------------")
# printGrid(getNextGrid(currentGrid, UP))
