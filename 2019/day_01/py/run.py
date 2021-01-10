#! /usr/bin/python3

import sys, os, time
from typing import List


def part1(masses: List[int]) -> int:
    return sum((mass // 3) - 2 for mass in masses)


def getFuel(mass: int) -> int:
    total = 0
    currentMass = mass
    while True:
        fuel = currentMass // 3 - 2
        if fuel <= 0:
            break
        total += fuel
        currentMass = fuel
    return total


def part2(masses: List[int]) -> int:
    return sum(getFuel(mass) for mass in masses)


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