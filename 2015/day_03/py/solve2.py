#! /usr/bin/python3

from common import getInput


def processDirection(visitedHouses, currentPosition, direction):
    x, y = direction
    currentPosition = (x + currentPosition[0], y + currentPosition[1])
    houseKey = str(currentPosition)
    if houseKey in visitedHouses:
        visitedHouses[houseKey] = visitedHouses[houseKey] + 1
    else:
        visitedHouses[houseKey] = 1
    return currentPosition


def main():
    santaVisitedHouses = {} 
    santaVisitedHouses[str((0, 0))] = 1
    robotVistedHouses = {}
    santaCurrentPosition = (0, 0)
    robotCurrentPosition = (0, 0)
    for index, direction in enumerate(getInput()):
        if index % 2:
            santaCurrentPosition = processDirection(santaVisitedHouses, santaCurrentPosition, direction)
        else:
            robotCurrentPosition = processDirection(robotVistedHouses, robotCurrentPosition, direction)

    print("Visited houses: ", len({**santaVisitedHouses, **robotVistedHouses}.keys()))


if __name__ == "__main__":
    main()
