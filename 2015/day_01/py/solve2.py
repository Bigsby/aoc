#! /usr/bin/python3

from common import getInput


def main():
    currentFloor = 0
    currentPosition = 1
    for direction in getInput():
        currentFloor = currentFloor + direction
        if currentFloor == -1:
            break
        currentPosition = currentPosition + 1

    print("Gonne to basement at position", currentPosition)


if __name__ == "__main__":
    main()
