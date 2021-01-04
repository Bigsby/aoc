#! /usr/bin/python3

import sys, os, time
from math import floor, sqrt
from itertools import cycle


def part1(targetNumber):
    side = floor(sqrt(targetNumber)) + 1
    pastLastSquare = targetNumber - (side - 1) ** 2
    halfSide = side // 2
    if pastLastSquare >= side:
        pastLastSquare -= side
    offsetToMiddle = abs(halfSide - pastLastSquare)
    return halfSide + offsetToMiddle


DIRECTIONS = [
    - 1 - 1j,
        - 1j,
    + 1 - 1j,
    - 1,
    + 1,
    - 1 + 1j,
        + 1j,
    + 1 + 1j
]
def getNeighbors(pos):
    for direction in DIRECTIONS:
        yield pos + direction


def getSumForNeighbors(grid, pos):
    total = 0
    for neighbor in getNeighbors(pos):
        total += grid[neighbor] if neighbor in grid else 0
    return total


def part2(target):
    grid = {
        0j: 1
    }
    newValue = 0
    position = 0j
    move = 1
    movesInDirection = 1
    while True:
        for _ in range(2):
            move *= 1j
            for _ in range(movesInDirection):
                position += move
                grid[position] = newValue = getSumForNeighbors(grid, position)
                if newValue > target:
                    return newValue
        movesInDirection += 1


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