#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Range = Tuple[int,int]


def solve(ranges: List[Range]) -> Tuple[int,int]:
    part1Result = 0
    ranges.sort()
    previousUpper = 0
    allowedCount = 0
    for lower, upper in ranges:
        if upper <= previousUpper:
            continue
        if lower > previousUpper + 1:
            allowedCount += lower - previousUpper - 1
            if part1Result == 0:
                part1Result = previousUpper + 1
        previousUpper = upper
    return part1Result, allowedCount


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()