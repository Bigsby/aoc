#! /usr/bin/python3

import sys, os, time
from typing import List

Instruction = List[str]


def part1(instructions: List[Instruction]) -> int:
    target = int(instructions[1][1]) * int(instructions[2][1])
    a = 1
    while a < target:
        if a % 2 == 0:
            a = a * 2 + 1
        else:
            a *= 2
    return a - target


def part2(puzzleInput):
    pass


def parseLine(line: str) -> Instruction:
    mnemonic = line[:3]
    parameters = line[3:].strip()
    return [ mnemonic ] + parameters.split(" ")


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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