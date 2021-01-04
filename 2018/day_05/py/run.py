#! /usr/bin/python3

import sys, os, time
import re


def part1(polymer):
    polymer = [ ord(c) for c in polymer]
    hadChanges = True
    while hadChanges:
        hadChanges = False
        index = 0
        while index < len(polymer) - 1:
            if abs(polymer[index] - polymer[index + 1]) == 32:
                del polymer[index]
                del polymer[index]
                hadChanges = True
            else:      
                index += 1
    return len(polymer)


def part2(polymer):
    minUnits = sys.maxsize
    for cOrd in range(ord("A"), ord("Z") + 1):
        strippedPolymer = re.sub("".join([ "[", chr(cOrd), chr(cOrd + 32), "]" ]), "", polymer)
        minUnits = min(minUnits, part1(strippedPolymer))
    return minUnits


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()