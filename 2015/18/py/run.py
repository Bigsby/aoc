#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, List, Tuple

Grid = Dict[complex,bool]
NEIGHBOR_DIRECTIONS: List[complex] = [
     - 1 - 1j,
         - 1j,
     + 1 - 1j,
     - 1,
     + 1,
     - 1 + 1j,
         + 1j,
     + 1 + 1j
]
def getNeighbors(pos: complex) -> Iterable[complex]:
    for direction in NEIGHBOR_DIRECTIONS:
        yield pos + direction


def getNextState(grid: Grid, alwaysOn: List[complex]) -> Grid:
    for position in alwaysOn:
            grid[position] = True
    newState = dict(grid)
    for position in grid:
        neighbors = sum(map(lambda neighbor: grid[neighbor] if neighbor in grid else 0, getNeighbors(position)))
        if grid[position]:
            newState[position] = neighbors == 2 or neighbors == 3
        else:
            newState[position] = neighbors == 3
    for position in alwaysOn:
            newState[position] = True
    return newState


def runSteps(grid: Grid, alwaysOn: List[complex] = []) -> int:
    for _ in range(100):
        grid = getNextState(grid, alwaysOn)
    return sum(grid.values())


def solve(grid: Grid) -> Tuple[int,int]:
    side = max(map(lambda key: key.real, grid.keys()))
    alwaysOn: List[complex] = [
        0,
        side * 1j,
        side,
        side * (1 + 1j)
    ]
    return (
        runSteps(grid), 
        runSteps(grid, alwaysOn)
    )


def getInput(filePath: str) -> Grid:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = Grid()
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = c == "#"
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