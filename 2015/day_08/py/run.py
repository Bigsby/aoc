#! /usr/bin/python3

import sys, os, time
from typing import Callable, List
import re
from functools import reduce


def countDifferences(puzzleInput: List[str], differencesFunc: Callable[[str],int]):
    return reduce(lambda soFar, s: soFar + differencesFunc(s), puzzleInput, 0)


hexaRegex = re.compile(r"\\x[0-9a-f]{2}")
def getStringDifference1(string: str):
    totalLength = len(string)
    stripped = string.replace(r"\\", "r")
    stripped = stripped.replace(r"\"", "r")
    stripped = hexaRegex.sub("r", stripped)
    stripped = stripped.strip(r"\"")
    return totalLength - len(stripped) 


def part1(puzzleInput: List[str]):
    return countDifferences(puzzleInput, getStringDifference1)


def getStringDifference2(string: str):
    initialLength = len(string)
    escaped = re.escape(string)
    escaped = escaped.replace("\"", "\\\"")
    return 2 + len(escaped) - initialLength


def part2(puzzleInput: List[str]):
    return countDifferences(puzzleInput, getStringDifference2)


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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