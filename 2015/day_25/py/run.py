#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re

FIRST_CODE = 20151125
MULTIPLIER = 252533
DIVIDER = 33554393


def part1(data: Tuple[int,int]) -> int:
    targetRow, targetColumn = data
    lastCode = FIRST_CODE
    currentLength = 1
    while True:
        column = 0
        currentLength += 1
        row = currentLength
        while row:
            column += 1
            lastCode = (lastCode * MULTIPLIER) % DIVIDER
            if column == targetColumn and row == targetRow:
                return lastCode
            row -= 1
            

def part2(puzzleInput):
    pass


def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return tuple(map(int, re.findall("\d+", file.read())))


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