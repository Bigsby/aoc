#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple

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


def solve(grid: Grid) -> Tuple[int,int]:
    previousValues = [ grid ]
    total = 10 ** 9
    minute = 0
    part1Result = 0
    while minute < total:
        if minute == 10:
            part1Result = getResourceValue(grid)
        minute += 1
        grid = getNextMinute(grid)
        if grid in previousValues:
            period = minute - previousValues.index(grid)
            minute += ((total - minute) // period) * period
        previousValues.append(grid)
    return part1Result, getResourceValue(grid)

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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()