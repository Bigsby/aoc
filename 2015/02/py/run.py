#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


def part1(dimensions: List[Tuple[int,int,int]]) -> int:
    totalPaper = 0
    for w, l, h in dimensions:
        wl = w * l
        wh = w * h
        hl = h * l
        smallest = min(wl, wh, hl)
        totalPaper += 2 * (wl + wh + hl) + smallest
    return totalPaper


def part2(dimensions: List[Tuple[int,int,int]]) -> int:
    totalRibbon = 0
    for w, l, h in dimensions:
        sidesList = [w, l, h]
        sidesList.remove(max(sidesList))
        totalRibbon += 2 * (sidesList[0] + sidesList[1]) + w * l * h
    return totalRibbon


def solve(dimensions: List[Tuple[int,int,int]]) -> Tuple[int,int]:
    return (part1(dimensions), part2(dimensions))


lineRegex = re.compile(r"^(\d+)x(\d+)x(\d+)$")
def parseLine(line:str) -> Tuple[int,int,int]:
    match = lineRegex.match(line)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Tuple[int,int,int]]:
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