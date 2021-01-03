#! /usr/bin/python3

import sys, os, time
import re
from itertools import product

def getCoveredPoints(claims):
    coveredPoints = {}
    for _, left, top, width, height in claims:
        for point in product(range(left, left + width), range(top, top + height)):
            if point in coveredPoints:
                coveredPoints[point] += 1
            else:
                coveredPoints[point] = 1
    return coveredPoints


def part1(claims):
    coveredPoints = getCoveredPoints(claims)
    return sum([ 1 for value in coveredPoints.values() if value > 1 ])


def part2(claims):
    coveredPoints = getCoveredPoints(claims)
    for id, left, top, width, height in claims:
        if all([ coveredPoints[point] == 1 for point in product(range(left, left + width), range(top, top + height)) ]):
            return id
        

lineRegex = re.compile(r"^#(?P<id>\d+)\s@\s(?P<left>\d+),(?P<top>\d+):\s(?P<width>\d+)x(?P<height>\d+)$")
def parseLine(line):
    match = lineRegex.match(line)
    return (
        int(match.group("id")),
        int(match.group("left")),
        int(match.group("top")),
        int(match.group("width")),
        int(match.group("height"))
    )


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