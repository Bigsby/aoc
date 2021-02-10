#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, Tuple
from enum import Enum


class State(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


Grid = Dict[complex,State]
NeighborFinder = Callable[[Grid,complex,complex],complex]


NEIGHBOR_DIRECTIONS = [
     - 1 - 1j,
         - 1j,
     + 1 - 1j,
     - 1,
     + 1,
     - 1 + 1j,
         + 1j,
     + 1 + 1j
]
def getOccupiedCount(grid: Grid, position: complex, getNeighborFunc: NeighborFinder) -> int:
    total = 0
    for direction in NEIGHBOR_DIRECTIONS:
        neighbor = getNeighborFunc(grid, position, direction)
        if neighbor in grid and grid[neighbor] == State.OCCUPIED:
            total += 1
    return total


def getPositionNewState(grid: Grid, position: complex, tolerance: int, getNeighborFunc: NeighborFinder) -> Tuple[bool,State]:
    currentState = grid[position]
    if currentState == State.FLOOR:
        return False, State.FLOOR
    occupiedCount = getOccupiedCount(grid, position, getNeighborFunc)
    if currentState == State.EMPTY and occupiedCount == 0:
        return True, State.OCCUPIED
    if currentState == State.OCCUPIED and occupiedCount > tolerance:
        return True, State.EMPTY
    return False, currentState


def getNextState(grid: Grid, tolerance: int, getNeighborFunc: NeighborFinder) -> Tuple[int,Grid]:
    newState = dict(grid)
    changedCount = 0
    for position in grid:
        changed, newPositionState = getPositionNewState(grid, position, tolerance, getNeighborFunc)
        changedCount += changed
        newState[position] = newPositionState
    return changedCount, newState
        

def runGrid(grid: Grid, tolerance: int, getNeighborFunc: NeighborFinder) -> int:
    grid = dict(grid)
    changed = 1
    while changed:
        changed, grid = getNextState(grid, tolerance, getNeighborFunc)
    return sum(map(lambda value: 1 if value == State.OCCUPIED else 0, grid.values()))


def part1(grid: Grid) -> int:
    return runGrid(grid, 3, lambda _, position, direction: position + direction)


def getDirectionalNeighbor(grid: Grid, position: complex, direction: complex) -> complex:
    position += direction
    while position in grid and grid[position] == State.FLOOR:
        position += direction
    return position


def part2(grid: Grid) -> int:
    return runGrid(grid, 4, getDirectionalNeighbor)


def getInput(filePath: str) -> Grid:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = State(c)
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