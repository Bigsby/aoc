#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from itertools import product

Claim = Tuple[int,int,int,int,int]


def getCoveredPoints(claims: List[Claim]) -> Dict[Tuple[int,int],int]:
    coveredPoints: Dict[Tuple[int,int],int] = {}
    for _, left, top, width, height in claims:
        for point in product(range(left, left + width), range(top, top + height)):
            if point in coveredPoints:
                coveredPoints[point] += 1
            else:
                coveredPoints[point] = 1
    return coveredPoints


def part2(claims: List[Claim], coveredPoints: Dict[Tuple[int,int],int]) -> int:
    for id, left, top, width, height in claims:
        if all(coveredPoints[point] == 1 for point in product(range(left, left + width), range(top, top + height))):
            return id
    raise Exception("Claim not found")


def solve(claims: List[Claim]) -> Tuple[int,int]:
    coveredPoints = getCoveredPoints(claims)
    return (
        sum([ 1 for value in coveredPoints.values() if value > 1 ]),
        part2(claims, coveredPoints)
    )


lineRegex = re.compile(r"^#(?P<id>\d+)\s@\s(?P<left>\d+),(?P<top>\d+):\s(?P<width>\d+)x(?P<height>\d+)$")
def parseLine(line: str) -> Claim:
    match = lineRegex.match(line)
    if match:
        return (
            int(match.group("id")),
            int(match.group("left")),
            int(match.group("top")),
            int(match.group("width")),
            int(match.group("height"))
        )
    raise Exception("Bad format", line)
    

def getInput(filePath: str) -> List[Claim]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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