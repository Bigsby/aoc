#! /usr/bin/python3

from common import getInput


def main():
    visitedHouses = {} 
    visitedHouses[str((0, 0))] = 1
    currentPosition = (0, 0)
    for direction in getInput():
        x, y = direction
        currentPosition = (x + currentPosition[0], y + currentPosition[1])
        houseKey = str(currentPosition)
        if houseKey in visitedHouses:
            visitedHouses[houseKey] = visitedHouses[houseKey] + 1
        else:
            visitedHouses[houseKey] = 1

    print("Visited houses: ", len(visitedHouses.keys()))


if __name__ == "__main__":
    main()
