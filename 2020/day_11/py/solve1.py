#! /usr/bin/python3

from common import getInput, State


def main():
    grid = getInput()
    updatedCount = 1
    iterations = 0
    while updatedCount != 0:
        iterations += 1
        updatedCount = grid.goToNextState()

    print("Iterations:", iterations)
    print("Occupied count:", grid.getOccupiedCount())


if __name__ == "__main__":
    main()
