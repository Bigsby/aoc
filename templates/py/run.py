#! /usr/bin/python3

import sys, os, time
from typing import Tuple


def part1(puzzleInput):
    pass


def part2(puzzleInput):
    pass


def solve(puzzleInput) -> Tuple[int,int]:
    return (part1(puzzleInput), part2(puzzleInput))


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath) as file:
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