#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


def calculateValue(text, one):
        value = 0
        for index, c in enumerate(text[::-1]):
            if c == one:
                value = value + pow(2, index)
        return value


class BoardingPass:
    def __init__(self, rowText, columnText):
        self.rowText = rowText
        self.columnText = columnText
        self.row = calculateValue(rowText, "B")
        self.column = calculateValue(columnText, "R")
        self.id = self.row * 8 + self.column


def part1(puzzleInput):
    return reduce(lambda currentMax, bp: max(currentMax, bp.id), puzzleInput, 0)


def part2(puzzleInput):
    boardingPasses = sorted(puzzleInput, key=lambda bp: bp.id)
    mySeatId = boardingPasses[0].id
    for bp in boardingPasses:
        if bp.id - mySeatId == 2:
            return mySeatId + 1
        mySeatId = bp.id


lineRegex = re.compile("^([BF]{7})([LR]{3})$")
def parseLine(line):
    match = lineRegex.match(line)
    return BoardingPass(match.group(1), match.group(2))


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