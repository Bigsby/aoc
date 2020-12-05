#! /usr/bin/python3

from common import getInput


def main():
    directions = getInput()

    currentFloor = 0
    for direction in directions:
        currentFloor = currentFloor + direction

    print("Final floor:", currentFloor)



if __name__ == "__main__":
    main()
