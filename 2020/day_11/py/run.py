#! /usr/bin/python3

import sys, os, time
from enum import Enum
from functools import reduce


class State(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


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
def getOccupiedCount(grid, position, getNeighborFunc):
    total = 0
    for direction in NEIGHBOR_DIRECTIONS:
        neighbor = getNeighborFunc(grid, position, direction)
        if neighbor in grid and grid[neighbor] == State.OCCUPIED:
            total += 1
    return total


def getPositionNewState(grid, position, tolerance, getNeighborFunc):
    currentState = grid[position]
    if currentState == State.FLOOR:
        return False, State.FLOOR
    occupiedCount = getOccupiedCount(grid, position, getNeighborFunc)
    if currentState == State.EMPTY and occupiedCount == 0:
        return True, State.OCCUPIED
    if currentState == State.OCCUPIED and occupiedCount > tolerance:
        return True, State.EMPTY
    return False, currentState


def getNextState(grid, tolerance, getNeighborFunc):
    newState = dict(grid)
    changedCount = 0
    for position in grid:
        changed, newPositionState = getPositionNewState(grid, position, tolerance, getNeighborFunc)
        changedCount += changed
        newState[position] = newPositionState
    return changedCount, newState
        

def runGrid(grid, tolerance, getNeighborFunc):
    grid = dict(grid)
    changed = 1
    while changed:
        changed, grid = getNextState(grid, tolerance, getNeighborFunc)
    return sum(map(lambda value: 1 if value == State.OCCUPIED else 0, grid.values()))


def part1(grid):
    return runGrid(grid, 3, lambda _, position, direction: position + direction)


def getDirectionalNeighbor(grid, position, direction):
    position += direction
    while position in grid and grid[position] == State.FLOOR:
        position += direction
    return position


def part2(grid):
    return runGrid(grid, 4, getDirectionalNeighbor)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = {}
        pos = 0j
        for line in file.readlines():
            for c in line.strip():
                grid[pos] = State(c)
                pos += 1
            pos += 1j - pos.real
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