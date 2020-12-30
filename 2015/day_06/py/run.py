#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


def getTurnedOn(matrix):
    return reduce(lambda rowCount, row: rowCount + reduce(lambda columnCount, column: columnCount + column, row), matrix, 0)


def runMatrix(updateFunc, puzzleInput):
    matrix = [ [0] * 1000 for i in range(1000) ]
    for action, xstart, ystart, xend, yend in puzzleInput:
        updateFunc(matrix, action, xstart, ystart, xend, yend) 
    return getTurnedOn(matrix)


def updateMatrix1(matrix, action, xstart, ystart, xend, yend):
    actionFun = lambda _: 0
    if action == "turn on":
        actionFun = lambda _: 1
    elif action == "toggle":
        actionFun = lambda value: 0 if value else 1

    for x in range(xstart, xend + 1):
        for y in range(ystart, yend + 1):
            matrix[x][y] = actionFun(matrix[x][y])


def part1(puzzleInput):
    return runMatrix(updateMatrix1, puzzleInput)


def updateMatrix2(matrix, action, xstart, ystart, xend, yend):
    actionFun = lambda value: value - 1 if value > 0 else 0
    if action == "turn on":
        actionFun = lambda value: value + 1
    elif action == "toggle":
        actionFun = lambda value: value + 2 

    for x in range(xstart, xend + 1):
        for y in range(ystart, yend + 1):
            matrix[x][y] = actionFun(matrix[x][y])


def part2(puzzleInput):
    return runMatrix(updateMatrix2, puzzleInput)


instructionRegex = re.compile("^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$")
def parseLine(line):
    match = instructionRegex.match(line)
    return (match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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