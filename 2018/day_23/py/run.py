#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Nanobot = Tuple[int,int,int,int]


def part1(nanobots: List[Nanobot]) -> int:
    maxRadius = 0
    strongestBot = (0, 0, 0, 0)
    for nanobot in nanobots:
        if nanobot[3] > maxRadius:
            maxRadius = nanobot[3]
            strongestBot = nanobot
    
    x0, y0, z0, radius = strongestBot
    inRange = 0
    for nanobot in nanobots:
        x1, y1, z1, _ = nanobot
        inRange += abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1) <= radius
    return inRange


def part2(nanobots: List[Nanobot]) -> int:
    xs = [bot[0] for bot in nanobots] + [0]
    ys = [bot[1] for bot in nanobots] + [0]
    zs = [bot[2] for bot in nanobots] + [0]
    locationRadius = 1
    while locationRadius < max(xs) - min(xs):
        locationRadius *= 2

    while True:
        hightestCount = 0
        bestLocation: Tuple[int,int,int] = (0,0,0)
        shortestDistance = -1
        for x in range(min(xs), max(xs) + 1, locationRadius):
            for y in range(min(ys), max(ys) + 1, locationRadius):
                for z in range(min(zs), max(zs) + 1, locationRadius):
                    count = 0
                    for botX, botY, botZ, botRadius in nanobots:
                        botDistance = abs(x - botX) + abs(y - botY) + abs(z - botZ)
                        if (botDistance - botRadius) // locationRadius <= 0:
                            count += 1
                    locationDistance = abs(x) + abs(y) + abs(z)
                    if count > hightestCount or (count == hightestCount and (shortestDistance == -1 or locationDistance < shortestDistance)):
                        hightestCount = count
                        shortestDistance = locationDistance
                        bestLocation = (x, y, z)

        if locationRadius == 1:
            return shortestDistance
        else:
            xs = [bestLocation[0] - locationRadius, bestLocation[0] + locationRadius]
            ys = [bestLocation[1] - locationRadius, bestLocation[1] + locationRadius]
            zs = [bestLocation[2] - locationRadius, bestLocation[2] + locationRadius]
            locationRadius = locationRadius // 2


def parseLine(line: str) -> Nanobot:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def getInput(filePath: str):
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