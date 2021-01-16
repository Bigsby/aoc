#! /usr/bin/python3

import sys, os, time
from typing import List
import re


class Disc():
    def __init__(self, positions: int, start: int, index: int):
        self.positions = positions
        self.offset = start + index + 1


def findWinningPosiiton(discs: List[Disc]):
    jump = 1
    offset = 0
    for disc in discs:
        while (offset + disc.offset) % disc.positions:
            offset += jump
        jump *= disc.positions
    return offset


def part1(discs: List[Disc]):
    return findWinningPosiiton(discs)


def part2(discs: List[Disc]):
    discs.append(Disc(11, 0, len(discs)))
    return findWinningPosiiton(discs)


lineRegex = re.compile(r"^Disc #\d has (?P<positions>\d+) positions; at time=0, it is at position (?P<start>\d+).$")
def parseLine(line: str, index: int) -> Disc:
    match = lineRegex.match(line)
    if match:
        positions = int(match.group("positions"))
        start = int(match.group("start"))
        return Disc(positions, start, index)
    raise Exception("Bad format", line)

    
def getInput(filePath: str) -> List[Disc]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line, index) for index, line in enumerate(file.readlines()) ]


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