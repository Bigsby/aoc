#! /usr/bin/python3

import sys, os, time
from typing import List


def part1(changes: List[int]) -> int:
    return sum(changes)


def part2(changes: List[int]):
    changesLength = len(changes)
    frequency = 0
    previous = set() 
    index = 0
    while frequency not in previous:
        previous.add(frequency)
        frequency += changes[index]
        index = (index + 1) % changesLength

    return frequency


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