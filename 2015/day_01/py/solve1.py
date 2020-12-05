#! /usr/bin/python3

from common import getInput


def main():
    directions = getInput()

    currentFloor = 0
    directionCount = 0
    for direction in directions:
        directionCount = directionCount + 1
        currentFloor = currentFloor + direction

    print("Final floor:", currentFloor)



if __name__ == "__main__":
    main()
