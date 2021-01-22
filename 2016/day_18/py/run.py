#! /usr/bin/python3

import sys, os, time
from typing import Dict


Grid = Dict[complex,bool]


def createRowsAndCount(grid: Grid, count: int):
    grid = dict(grid)
    maxX = int(max(map(lambda p: p.real, grid.keys())))
    for y in range(1, count):
        for x in range(maxX + 1):
            position = x + y * 1j
            leftPosition = position - 1 - 1j
            rightPosition = position + 1 - 1j
            left = leftPosition in grid and grid[leftPosition]
            rigth = rightPosition in grid and grid[rightPosition]
            grid[position] = left ^ rigth
    return sum(not value for value in grid.values())


def part1(grid: Grid):
    return createRowsAndCount(grid, 40)


def part2(grid: Grid):
    return createRowsAndCount(grid, 400000)


def getInput(filePath: str) -> Grid:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = {}
        for index, c in enumerate(file.read().strip()):
            grid[index + 0j] = c == "^"
        return grid


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