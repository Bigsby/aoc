#! /usr/bin/python3

import sys, os, time
from typing import List
from functools import reduce
from itertools import combinations


def getMinimumGroupEntanglement(weights: List[int], groupCount: int) -> int:
    groupWeight = sum(weights) // groupCount
    for size in range(1, len(weights)):
        entanglements = [ reduce(lambda soFar, weight: soFar * weight, group) \
            for group in combinations(weights, size) if sum(group) == groupWeight ]
        if entanglements:
            return min(entanglements)
    raise Exception("Group not found")


def part1(weights: List[int]) -> int:
    return getMinimumGroupEntanglement(weights, 3)


def part2(weights: List[int]) -> int:
    return getMinimumGroupEntanglement(weights, 4)


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line.strip()) for line in file.readlines() ]


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