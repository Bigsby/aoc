#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


FIRST_CODE = 20151125
MULTIPLIER = 252533
DIVIDER = 33554393
def solve(data: Tuple[int,int]) -> Tuple[int,str]:
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
                return (lastCode, "")
            row -= 1


def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return tuple(map(int, re.findall(r"\d+", file.read())))


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