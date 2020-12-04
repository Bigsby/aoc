#! /usr/bin/python3

from common import getInput


def main():
    directions = getInput()

    currentFloor = 0
    directionCount = 0
    for c in directions:
        directionCount = directionCount + 1
        if c == '(':
            currentFloor = currentFloor + 1
        elif c == ')':
            currentFloor = currentFloor - 1

    print("Final floor:", currentFloor)



if __name__ == "__main__":
    main()
