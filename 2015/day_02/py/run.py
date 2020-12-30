#! /usr/bin/python3

import sys, os, time
import re


def part1(puzzleInput):
    totalPaper = 0
    for dimension in puzzleInput:
        w, l, h = dimension
        wl = w * l
        wh = w * h
        hl = h * l
        smallest = min(wl, wh, hl)
        totalPaper = totalPaper + (2 * wl) + (2 * wh) + (2 * hl) + smallest

    return totalPaper


def part2(puzzleInput):
    totalRibbon = 0
    for dimension in puzzleInput:
        w, l, h = dimension
        sidesList = [w, l, h]
        sidesList.remove(max(sidesList))
        totalRibbon = totalRibbon + 2 * sidesList[0] + 2 * sidesList[1] + w * l * h

    return totalRibbon


lineRegex = re.compile("^(\d+)x(\d+)x(\d+)$")
def parseLine(line):
    match = lineRegex.match(line)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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