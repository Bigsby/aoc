#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple
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


def solve(serialNumber: int) -> Tuple[str,str]:
    grid = buildGrid(serialNumber)
    summedAreaTable = buildSummedAreaTable(grid)
    maxFuel = maxSize = 0
    maxCell = (-1, -1)
    max3Cell = (-1, -1)
    max3Fuel = 0
    for size in range(1, GRID_SIZE):
        for y, x in product(range(1, GRID_SIZE - size), range(1, GRID_SIZE - size)):
            fuel = sumFromAreaTable(summedAreaTable, x, y, size)
            if fuel > maxFuel:
                maxFuel = fuel
                maxCell = x + 1, y + 1
                maxSize = size
            if size == 3 and fuel > max3Fuel:
                max3Fuel = fuel
                max3Cell = x + 1, y + 1
    return f"{max3Cell[0]},{max3Cell[1]}", f"{maxCell[0]},{maxCell[1]},{maxSize}"
    

def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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