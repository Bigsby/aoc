#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple
import re


def countDifferences(puzzleInput: List[str], differencesFunc: Callable[[str],int]):
    return sum(differencesFunc(s) for s in puzzleInput)


hexaRegex = re.compile(r"\\x[0-9a-f]{2}")
def getStringDifference1(string: str) -> int:
    totalLength = len(string)
    stripped = string.replace(r"\\", "r")
    stripped = stripped.replace(r"\"", "r")
    stripped = hexaRegex.sub("r", stripped)
    stripped = stripped.strip(r"\"")
    return totalLength - len(stripped) 


def getStringDifference2(string: str) -> int:
    initialLength = len(string)
    escaped = re.escape(string)
    escaped = escaped.replace("\"", "\\\"")
    return 2 + len(escaped) - initialLength


def solve(puzzleInput: List[str]) -> Tuple[int,int]:
    return (countDifferences(puzzleInput, getStringDifference1), countDifferences(puzzleInput, getStringDifference2))


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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