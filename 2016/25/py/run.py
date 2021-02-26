#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Instruction = List[str]


def solve(instructions: List[Instruction]) -> Tuple[int,str]:
    target = int(instructions[1][1]) * int(instructions[2][1])
    a = 1
    while a < target:
        if a % 2 == 0:
            a = a * 2 + 1
        else:
            a *= 2
    return a - target, ""


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()