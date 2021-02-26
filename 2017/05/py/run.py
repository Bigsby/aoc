#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple


def doJumps(jumps: List[int], newJumpFunc: Callable[[int],int]) -> int:
    jumps = list(jumps)
    maxIndex = len(jumps)
    currentIndex = 0
    count = 0
    while currentIndex >= 0 and currentIndex < maxIndex:
        count += 1
        offset = jumps[currentIndex]
        nextIndex = currentIndex + offset
        jumps[currentIndex] = offset + newJumpFunc(offset)
        currentIndex = nextIndex
    return count


def solve(jumps: List[int]) -> Tuple[int,int]:
    return (
        doJumps(jumps, lambda _: 1),
        doJumps(jumps, lambda offset: 1 if offset < 3 else -1)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line) for line in file.readlines() ]


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