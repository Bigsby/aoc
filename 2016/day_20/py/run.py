#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Range = Tuple[int,int]


def part1(ranges: List[Range]) -> int:
    ranges.sort()
    rangeIter = iter(ranges)
    previousUpper = 0
    while True:
        lower, upper = next(rangeIter)
        if upper <= previousUpper:
            continue
        if lower <= previousUpper + 1:
            previousUpper = upper
        else:
            return previousUpper + 1


def part2(ranges: List[Range]) -> int:
    ranges.sort()
    previousUpper = 0
    allowedCount = 0
    for lower, upper in ranges:
        if upper <= previousUpper:
            continue
        if lower > previousUpper + 1:
            allowedCount += lower - previousUpper - 1
        previousUpper = upper
    return allowedCount


def parseLine(line: str) -> Range:
    splits = line.strip().split("-")
    return int(splits[0]), int(splits[1])


def getInput(filePath: str) -> List[Range]:
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