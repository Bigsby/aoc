#! /usr/bin/python3

import sys, os, time
from typing import Callable, List


def doJumps(jumps: List[int], newJumpFunc: Callable[[int],int]) -> int:
    jumps = list(jumps)
    maxIndex = len(jumps)
    currentIndex = 0
    count = 0
    while currentIndex >= 0 and currentIndex < maxIndex:
        count += 1
        offset = jumps[currentIndex]
        nextIndex = currentIndex + offset
        jumps[currentIndex] = newJumpFunc(offset)
        currentIndex = nextIndex
    return count


def part1(jumps: List[int]) -> int:
    return doJumps(jumps, lambda offset: offset + 1)


def part2(jumps: List[int]) -> int:
    return doJumps(jumps, lambda offset: offset + (1 if offset < 3 else - 1))


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line) for line in file.readlines() ]


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