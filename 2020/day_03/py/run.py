#! /usr/bin/python3

import sys, os, time
from functools import reduce


def calculateTrees(grid, step):
    lastRow = len(grid)
    lastColumn = len(grid[0])
    currentPosition = (0, 0)
    treeCount = 0
    while currentPosition[0] < lastRow:
        treeCount = treeCount + grid[currentPosition[0]][currentPosition[1] % lastColumn]
        currentPosition = (currentPosition[0] + step[0], currentPosition[1] + step[1])
    return treeCount


def part1(puzzleInput):
    treeCount = calculateTrees(puzzleInput, (1, 3))
    return treeCount


def part2(puzzleInput):
    steps = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
       ]
    return reduce(lambda current, step: current * calculateTrees(puzzleInput, step), steps, 1)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    grid = []
    with open(filePath, "r") as file:
        for line in file.readlines():
            row = []
            for c in line:
                if c == '#':
                    row.append(1)
                elif c == '.':
                    row.append(0)
                elif c == '\n':
                    break 
                else:
                    raise Exception("Unrecognized character in input", str(ord(c)))
            grid.append(row)
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