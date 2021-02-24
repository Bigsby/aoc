#! /usr/bin/python3

import sys, os, time
from typing import List

Instruction = List[str]


def part1(number: int) -> int:
    return (number - 2) ** 2


def part2(number: int) -> int:
    total =  number * 100 + 100000
    nonPrimes = 0
    for candidate in range(total, total + 17000 + 1, 17):
        divider = 2
        while candidate % divider != 0:
            divider += 1
        nonPrimes += candidate != divider
    return nonPrimes


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.readlines()[0].split(" ")[2])


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