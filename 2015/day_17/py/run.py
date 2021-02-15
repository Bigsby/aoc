#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import combinations


TARGET_TOTAL = 150
def getValidCombinations(containers: List[int]) -> List[Tuple[int,...]]:
    validCombinations = []
    for containerCount in range(2, len(containers)):
        for combination in combinations(containers, containerCount):
            if sum(combination) == TARGET_TOTAL:
                validCombinations.append(combination)
    return validCombinations


def part1(containers: List[int]) -> int:
    return len(getValidCombinations(containers))


def part2(containers: List[int]) -> int:
    validCombinations = getValidCombinations(containers)
    minCount = min([ len(combination) for combination in validCombinations ])
    return len([ combination for combination in validCombinations if len(combination) == minCount ])


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