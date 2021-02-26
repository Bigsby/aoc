#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple


def processDirection(visitedHouses: Dict[complex,int], currentPosition: complex, direction: complex):
    currentPosition += direction
    if currentPosition in visitedHouses:
        visitedHouses[currentPosition] += 1
    else:
        visitedHouses[currentPosition] = 1
    return currentPosition


def part1(directions: List[complex]):
    visitedHouses = {} 
    visitedHouses[0] = 1
    currentPosition = 0
    for direction in directions:
        currentPosition = processDirection(visitedHouses, currentPosition, direction)
    return len(visitedHouses.keys())


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


def solve(directions: List[complex]) -> Tuple[int,int]:
    return (part1(directions), part2(directions))


DIRECTIONS = {
    "^": -1j,
    "v": 1j,
    ">": 1,
    "<": -1
}
def getInput(filePath: str) -> List[complex]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ DIRECTIONS[c] for c in file.read().strip() if c in DIRECTIONS ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()