#! /usr/bin/python3

import sys, os, time
from typing import Tuple


GROUP_START = "{"
GROUP_END = "}"
GARBAGE_START = "<"
GARBAGE_END = ">"
ESCAPE = "!"
def count(stream: str) -> Tuple[int,int]:
    groupScore = 0
    garbageCount = 0
    depth = 0
    inGarbage = False
    escape = False
    for c in stream:
        if escape:
            escape = False
        elif inGarbage:
            if c == ESCAPE:
                escape = True
            elif c == GARBAGE_END:
                inGarbage = False
            else:
                garbageCount += 1
        elif c == GARBAGE_START:
            inGarbage = True
        elif c == GROUP_START:
            depth += 1
        elif c == GROUP_END:
            groupScore += depth
            depth -= 1

    return groupScore, garbageCount


def part1(stream: str) -> int:
    return count(stream)[0]


def part2(stream: str) -> int:
    return count(stream)[1]


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read()


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