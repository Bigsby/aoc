#! /usr/bin/python3

import sys, os, time
from typing import Dict

Grid = Dict[complex,int]
Open, Tree, Lumberyard = 0, 1, 2
RESOURCES = {
    ".": Open,
    "|": Tree,
    "#": Lumberyard
}


NEIGHBOR_DIRECTIONS = [ -1 - 1j, -1j, +1 -1j, -1, +1, -1 + 1j, +1j, 1 + 1j ]
def getCountAround(position: complex, grid: Grid, state: int) -> int:
    return sum([ 1 for direction in NEIGHBOR_DIRECTIONS if position + direction in grid and grid[position + direction] == state ])


def getNextMinute(grid: Grid) -> Grid:
    newState: Grid = {}
    for position, state in grid.items():
        if state == Open:
            newState[position] = Tree if getCountAround(position, grid, Tree) > 2 else Open
        elif state == Tree:
            newState[position] = Lumberyard if getCountAround(position, grid, Lumberyard) > 2 else Tree
        elif state == Lumberyard:
            newState[position] = Lumberyard if getCountAround(position, grid, Lumberyard) > 0 and getCountAround(position, grid, Tree) > 0 else Open
    return newState


def getResourceValue(grid: Grid) -> int:
    return sum([ 1 for v in grid.values() if v == Tree ]) * sum([ 1 for v in grid.values() if v == Lumberyard ])


def part1(grid: Grid) -> int:
    for _ in range(10):
        grid = getNextMinute(grid)
    return getResourceValue(grid)


def part2(grid: Grid) -> int:
    previousValues = [ grid ]
    total = 10 ** 9
    minute = 0
    while minute < total:
        minute += 1
        grid = getNextMinute(grid)
        if grid in previousValues:
            period = minute - previousValues.index(grid)
            minute += ((total - minute) // period) * period
        previousValues.append(grid)
    return getResourceValue(grid)


def getInput(filePath: str) -> Grid:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid: Grid = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = RESOURCES[c]
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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()