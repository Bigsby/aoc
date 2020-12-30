#! /usr/bin/python3

import sys, os, time
from itertools import combinations


def getValidCombinations(containers):
    targetTotal = 150
    validCombinations = []
    for containerCount in range(2, len(containers)):
        for combination in combinations(containers, containerCount):
            if sum(combination) == targetTotal:
                validCombinations.append(combination)

    return validCombinations


def part1(puzzleInput):
    return len(getValidCombinations(puzzleInput))


def part2(puzzleInput):
    validCombinations = getValidCombinations(puzzleInput)
    minCount = min([ len(combination) for combination in validCombinations ])
    return len([ combination for combination in validCombinations if len(combination) == minCount ])


def getInput(filePath):
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