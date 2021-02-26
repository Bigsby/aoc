#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


testRegex = re.compile(r"(\d)\1+|\d")
def getNextValue(value: str) -> str:
    sequences = []
    for match in testRegex.finditer(value):
        group = match.group()
        sequences.append(str(len(group)))
        sequences.append(group[0])
    return "".join(sequences)


def solve(puzzleInput: str) -> Tuple[int,int]:
    currentValue = puzzleInput
    part1 = 0
    for turn in range(50):
        if turn == 40:
            part1 = len(currentValue)
        currentValue = getNextValue(currentValue)
    return (part1, len(currentValue))


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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