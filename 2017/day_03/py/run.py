#! /usr/bin/python3

import sys, os, time
from math import floor, sqrt
from itertools import cycle


def part1(targetNumber):
    side = floor(sqrt(targetNumber)) + 1
    excess = targetNumber - (side - 1) ** 2
    halfSide = side // 2
    if excess >= side:
        excess -= side
    sideOffset = abs(halfSide - excess)
    return halfSide + sideOffset


def getNeighbors(x, y):
    yield (x - 1, y - 1)
    yield (x    , y - 1)
    yield (x + 1, y - 1)
    yield (x - 1, y    )
    yield (x + 1, y    )
    yield (x - 1, y + 1)
    yield (x    , y + 1)
    yield (x + 1, y + 1)


moves = cycle([
    lambda x, y: (x + 1, y),
    lambda x, y: (x, y + 1), 
    lambda x, y: (x - 1, y), 
    lambda x, y: (x, y - 1)
])
def generateSpiralPositions(end):
    count = 1
    position = (0, 0)
    movesInDirection = 1
    while True:
        for _ in range(2):
            move = next(moves)
            for _ in range(movesInDirection):
                if count >= end:
                    return
                position = move(*position)
                count +=1
                yield position
        movesInDirection += 1


def part2(puzzleInput):
    side = 9
    grid = [ [ 0 for _ in range(side) ] for _ in range(side) ]
    middle = side // 2
    grid[middle][middle] = 1
    for x, y in generateSpiralPositions(side ** 2):
        ajustedX, ajustedY = (middle - x, middle - y)
        newValue = sum([ grid[x][y] for x, y in getNeighbors(ajustedX, ajustedY) ])
        if newValue > puzzleInput:
            return newValue
        grid[ajustedX][ajustedY] = newValue


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read())


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