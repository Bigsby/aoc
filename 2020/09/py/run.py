#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def hasNoValidPair(numberIndex: int, numbers: List[int]) -> bool:
    number = numbers[numberIndex]
    for testIndex in range(numberIndex - 25, numberIndex):
        testNumber = numbers[testIndex]
        for pairIndex in range(numberIndex - 25, numberIndex):
            if pairIndex != testIndex and testNumber + numbers[pairIndex] == number:
                return False
    return True


def getWeakness(numbers: List[int], targetNumber: int) -> int:
    for startIndex in range(0, len(numbers)):
        currentSum = 0
        length = 1
        while currentSum < targetNumber:
            newSet = numbers[startIndex:startIndex + length]
            currentSum = sum(newSet)
            if currentSum == targetNumber:
                return min(newSet) + max(newSet)
            length += 1
    raise Exception("Weakness not found")


def solve(numbers: List[int]) -> Tuple[int,int]:
    part1Result = next(numbers[index] for index in range(25, len(numbers)) if hasNoValidPair(index, numbers))
    return (
        part1Result,
        getWeakness(numbers, part1Result)
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