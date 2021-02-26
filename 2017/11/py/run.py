#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


def getHexManhatanDistance(position: complex) -> int:
    if (position.real > 0) ^ (position.imag > 0):
        return int(max(abs(position.real) , abs(position.imag)))
    return int(abs(position.real) +  abs(position.imag))


DIRECTIONS = {
    "s" :       1j,
    "se":   1     ,
    "sw": - 1 + 1j,
    "ne":   1 - 1j,
    "nw": - 1     ,
    "n" :     - 1j
}
def solve(instructions: List[str]) -> Tuple[int,int]:
    furthest = 0
    currentHex = 0
    for instrucion in instructions:
        currentHex += DIRECTIONS[instrucion]
        furthest = max(furthest, getHexManhatanDistance(currentHex))
    return getHexManhatanDistance(currentHex), furthest


instructionRegex = re.compile(r"ne|nw|n|sw|se|s")
def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ match.group() for match in instructionRegex.finditer(file.read()) ]


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