#! /usr/bin/python3

import sys, os, time
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


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()