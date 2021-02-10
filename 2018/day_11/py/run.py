#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, Tuple
from itertools import product

Grid = Dict[complex,int]
GRID_SIZE = 300


def calculatePowerLevel(x: int, y: int, serialNumber: int) -> int:
    rackId = x + 10
    powerLevel = rackId * y
    powerLevel += serialNumber
    powerLevel *= rackId
    powerLevel = powerLevel % 1000 // 100
    return powerLevel - 5


def buildGrid(serialNumber: int) -> Dict[complex,int]:
    return { x + y * 1j: calculatePowerLevel(x + 1, y + 1, serialNumber) for y, x in product(range(GRID_SIZE), range(GRID_SIZE)) }


def buildSummedAreaTable(grid: Grid) -> Grid:
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
              grid[x     +  y      * 1j ] = \
              grid[x     +  y      * 1j ] + \
            ( grid[x - 1 +  y      * 1j ] if x > 0 else 0 ) + \
            ( grid[x     + (y - 1) * 1j ] if y > 0 else 0) + \
            (-grid[x - 1 + (y - 1) * 1j ] if x > 0 and y > 0 else 0)    
    return grid


def sumFromAreaTable(grid: Grid, x: int, y: int, size: int) -> int:
    return  grid[x - 1        + (y - 1)        * 1j] \
          - grid[x - 1 + size + (y - 1)        * 1j] \
          - grid[x - 1        + (y - 1 + size) * 1j] \
          + grid[x - 1 + size + (y - 1 + size) * 1j]


def findLargestPower(serialNumber: int, sizes: Iterable[int]) -> Tuple[Tuple[int,int], int]:
    grid = buildGrid(serialNumber)
    summedAreaTable = buildSummedAreaTable(grid)
    maxFuel = maxSize = 0
    maxCell = (-1, -1)
    for size in sizes:
        for y, x in product(range(1, GRID_SIZE - size), range(1, GRID_SIZE - size)):
            fuel = sumFromAreaTable(summedAreaTable, x, y, size)
            if fuel > maxFuel:
                maxFuel = fuel
                maxCell = x + 1, y + 1
                maxSize = size
    return maxCell, maxSize


def part1(serialNumber: int) -> str:
    (x,y), _ = findLargestPower(serialNumber, [ 3 ])
    return f"{x},{y}"


def part2(serialNumber: int) -> str:
    (x, y), size = findLargestPower(serialNumber, range(1, GRID_SIZE))
    return f"{x},{y},{size}"


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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