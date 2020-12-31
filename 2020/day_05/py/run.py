#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


def calculateValue(text, one):
        value = 0
        for index, c in enumerate(text[::-1]):
            if c == one:
                value += 2 ** index
        return value


def part1(puzzleInput):
    return max(puzzleInput)


def part2(puzzleInput):
    ids = sorted(puzzleInput)
    lastId = ids[0]
    for currentId in ids:
        if currentId - lastId == 2:
            return lastId + 1
        lastId = currentId


lineRegex = re.compile("^([BF]{7})([LR]{3})$")
def parseLine(line):
    match = lineRegex.match(line)
    return calculateValue(match.group(1), "B") * 8 + calculateValue(match.group(1), "R")


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