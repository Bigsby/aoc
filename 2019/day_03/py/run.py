#! /usr/bin/python3

import sys, os, time
from typing import Iterable, List, Tuple
import re


Wire = List[Tuple[str,int]]
Position = complex

STEPS = {
    "R": 1,
    "U": -1j,
    "L": -1,
    "D": 1j
}
def getWirePositions(wire: Wire) -> Iterable[Position]:
    currentPosition = 0j
    for direction, distance in wire:
        step = STEPS[direction]
        for _ in range(distance):
            currentPosition += step
            yield currentPosition


def part1(wires: Tuple[Wire,Wire]) -> int:
    wireA, wireB = wires
    wireApoints = set(getWirePositions(wireA))
    return int(min([ abs(position.real) + abs(position.imag) for position in getWirePositions(wireB) if position in wireApoints ]))


def part2(wires: Tuple[Wire,Wire]) -> int:
    wireA, wireB = wires
    wireApoints = {}
    for steps, position in enumerate(getWirePositions(wireA)):
        if position in wireApoints:
            continue
        wireApoints[position] = steps + 1

    return min([ wireApoints[position] + steps + 1 for steps, position in enumerate(getWirePositions(wireB)) if position in wireApoints ])


lineRegex = re.compile(r"(?P<direction>R|U|L|D)(?P<distance>\d+)")
def parseLine(line: str) -> Wire:
    return [ (match.group("direction"), int(match.group("distance"))) for match in lineRegex.finditer(line) ]


def getInput(filePath: str) -> Tuple[Wire,Wire]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        lines = file.readlines()
        return parseLine(lines[0]), parseLine(lines[1])


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