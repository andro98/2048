from MinMax import *
import time

def main():
    time.sleep(2)
    # getGrid()
    # printGrid(currentGrid)
    while True:
        getGrid()
        createMiniMaxTtree(4)
        performMove(getMoves())
        time.sleep(0.2)

if __name__ == '__main__':
    main()