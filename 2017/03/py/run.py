#! /usr/bin/python3

import sys, os, time
from math import floor, sqrt
from typing import Dict, List, Tuple


def part1(targetNumber: int) -> int:
    side = floor(sqrt(targetNumber)) + 1
    pastLastSquare = targetNumber - (side - 1) ** 2
    halfSide = side // 2
    if pastLastSquare >= side:
        pastLastSquare -= side
    offsetToMiddle = abs(halfSide - pastLastSquare)
    return halfSide + offsetToMiddle


DIRECTIONS: List[complex] = [
    - 1 - 1j, - 1j, 1 - 1j,
    - 1,            1,
    - 1 + 1j,   1j, 1 + 1j
]
def getSumForNeighbors(grid: Dict[complex,int], position:complex) -> int:
    return sum(map(lambda neighbor: grid[neighbor] if neighbor in grid else 0, \
        map(lambda direction: position + direction, DIRECTIONS)))


def part2(target: int) -> int:
    grid: Dict[complex,int] = { 0j: 1 }
    position = 0j
    direction = 1
    movesInDirection = 1
    while True:
        for _ in range(2):
            direction *= 1j
            for _ in range(movesInDirection):
                position += direction
                grid[position] = getSumForNeighbors(grid, position)
                if grid[position] > target:
                    return grid[position]
        movesInDirection += 1


def solve(target: int) -> Tuple[int,int]:
    return (
        part1(target),
        part2(target)
    )


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read())


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