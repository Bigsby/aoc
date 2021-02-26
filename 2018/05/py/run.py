#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


def part1(polymer: str) -> int:
    polymerInts = [ ord(c) for c in polymer]
    hadChanges = True
    while hadChanges:
        hadChanges = False
        index = 0
        while index < len(polymerInts) - 1:
            if abs(polymerInts[index] - polymerInts[index + 1]) == 32:
                del polymerInts[index]
                del polymerInts[index]
                hadChanges = True
            else:      
                index += 1
    return len(polymerInts)


def part2(polymer: str) -> int:
    minUnits = sys.maxsize
    for cOrd in range(ord("A"), ord("Z") + 1):
        strippedPolymer = re.sub("".join([ "[", chr(cOrd), chr(cOrd + 32), "]" ]), "", polymer)
        minUnits = min(minUnits, part1(strippedPolymer))
    return minUnits


def solve(polymer: str) -> Tuple[int,int]:
    return (
        part1(polymer),
        part2(polymer)
    )


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