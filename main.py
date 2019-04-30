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


# print(swipeRow([2, 0, 2, 2]))
# getGrid()
# printGrid(currentGrid)
# print("-------------")
# printGrid(getNextGrid(currentGrid, UP))
