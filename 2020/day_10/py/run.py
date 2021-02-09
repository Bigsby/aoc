#! /usr/bin/python3

import sys, os, time
from typing import List
from functools import reduce


def part1(numbers: List[int]) -> int:
    diff1 = 0
    diff3 = 1
    currentJoltage = 0
    for number in sorted(numbers):
        diff = number - currentJoltage
        if diff == 1:
            diff1 += 1
        elif diff == 3:
            diff3 += 1
        currentJoltage = number
    return diff1 * diff3


def calculateCombinations(sequence: int) -> int:
    if sequence < 3:
        return 1
    if sequence == 3:
        return 2
    return calculateCombinations(sequence - 1) + calculateCombinations(sequence - 2) + calculateCombinations(sequence - 3)


def part2(numbers: List[int]) -> int:
    adapters = sorted(numbers)
    adapters.append(adapters[-1])
    sequences = []
    currentSequenceLength = 1
    currentJoltage = 0
    for joltage in adapters:
        if currentJoltage == joltage - 1:
            currentSequenceLength += 1
        else:
            sequences.append(currentSequenceLength)
            currentSequenceLength = 1
        currentJoltage = joltage
    return reduce(lambda soFar, length: soFar * calculateCombinations(length), sequences, 1)


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