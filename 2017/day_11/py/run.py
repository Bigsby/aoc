#! /usr/bin/python3

import sys, os, time
from typing import List
import re


def getHexManhatanDistance(position: complex) -> int:
    xSignal = True if position.real > 0 else False
    ySignal = True if position.imag > 0 else False
    if xSignal ^ ySignal:
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
def part1(instructions: List[str]):
    furthest = 0
    currentHex = 0
    for instrucion in instructions:
        currentHex += DIRECTIONS[instrucion]
        distance = getHexManhatanDistance(currentHex)
        furthest = max(furthest, distance)

    return getHexManhatanDistance(currentHex), furthest


def part2(result: int) -> int:
    return result


instructionRegex = re.compile(r"ne|nw|n|sw|se|s")
def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ match.group() for match in instructionRegex.finditer(file.read()) ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result, part2Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(part2Result)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()