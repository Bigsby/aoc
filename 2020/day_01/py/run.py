#! /usr/bin/python3

import sys, os, time
from typing import List
from itertools import combinations
from functools import reduce


def getCombination(numbers: List[int], length: int) -> int:
    for combination in combinations(numbers, length):
        if sum(combination) == 2020:
            return reduce(lambda soFar, number: soFar * number, combination)
    raise Exception("Numbers not found")


def part1(numbers: List[int]) -> int:
    return getCombination(numbers, 2)


def part2(numbers: List[int]) -> int:
    return getCombination(numbers, 3)


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()