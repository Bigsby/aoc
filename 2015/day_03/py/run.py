#! /usr/bin/python3

import sys, os, time


directions = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1,0)
    }


def part1(puzzleInput):
    visitedHouses = {} 
    visitedHouses[str((0, 0))] = 1
    currentPosition = (0, 0)
    for direction in puzzleInput:
        x, y = direction
        currentPosition = (x + currentPosition[0], y + currentPosition[1])
        houseKey = str(currentPosition)
        if houseKey in visitedHouses:
            visitedHouses[houseKey] = visitedHouses[houseKey] + 1
        else:
            visitedHouses[houseKey] = 1

    return len(visitedHouses.keys())


def processDirection(visitedHouses, currentPosition, direction):
    x, y = direction
    currentPosition = (x + currentPosition[0], y + currentPosition[1])
    houseKey = str(currentPosition)
    if houseKey in visitedHouses:
        visitedHouses[houseKey] = visitedHouses[houseKey] + 1
    else:
        visitedHouses[houseKey] = 1
    return currentPosition


def part2(puzzleInput):
    visitedHouses = {}
    visitedHouses[str((0, 0))] = 1
    santaCurrentPosition = (0, 0)
    robotCurrentPosition = (0, 0)
    for index, direction in enumerate(puzzleInput):
        if index % 2:
            santaCurrentPosition = processDirection(visitedHouses, santaCurrentPosition, direction)
        else:
            robotCurrentPosition = processDirection(visitedHouses, robotCurrentPosition, direction)

    return len(visitedHouses.keys())


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ directions[c] for c in file.read() if c in directions ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()