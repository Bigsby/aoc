#! /usr/bin/python3

import sys, os, time
from typing import Dict, List


directions = {
    "^": -1j,
    "v": 1j,
    ">": 1,
    "<": -1
    }


def part1(directions: List[complex]):
    visitedHouses = {} 
    visitedHouses[0] = 1
    currentPosition = 0
    for direction in directions:
        currentPosition += direction
        if currentPosition in visitedHouses:
            visitedHouses[currentPosition] += 1
        else:
            visitedHouses[currentPosition] = 1

    return len(visitedHouses.keys())


def processDirection(visitedHouses: Dict[complex,int], currentPosition: complex, direction: complex):
    currentPosition += direction
    houseKey = str(currentPosition)
    if houseKey in visitedHouses:
        visitedHouses[currentPosition] += 1
    else:
        visitedHouses[currentPosition] = 1
    return currentPosition


def part2(directions: List[complex]):
    visitedHouses = {}
    visitedHouses[0] = 1
    santaCurrentPosition = robotCurrentPosition = 0
    for index, direction in enumerate(directions):
        if index % 2:
            santaCurrentPosition = processDirection(visitedHouses, santaCurrentPosition, direction)
        else:
            robotCurrentPosition = processDirection(visitedHouses, robotCurrentPosition, direction)

    return len(visitedHouses.keys())


def getInput(filePath: str) -> List[complex]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ directions[c] for c in file.read().strip() if c in directions ]


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