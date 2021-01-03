#! /usr/bin/python3

import sys, os, time
import re


STEPS = {
    "R": 1,
    "U": -1j,
    "L": -1,
    "D": 1j
}
def getWirePoints(wire):
    currentPosition = 0j
    for direction, distance in wire:
        step = STEPS[direction]
        for _ in range(distance):
            currentPosition += step
            yield currentPosition


def part1(puzzleInput):
    wireA, wireB = puzzleInput
    wireApoints = set()
    for position in getWirePoints(wireA):
        wireApoints.add(position)
    
    minIntersectionDistance = sys.maxsize
    for position in getWirePoints(wireB):
        if position in wireApoints:
            minIntersectionDistance = min(minIntersectionDistance, abs(position.real) + abs(position.imag))
    
    return int(minIntersectionDistance)


def part2(puzzleInput):
    wireA, wireB = puzzleInput
    wireApoints = {}
    for steps, position in enumerate(getWirePoints(wireA)):
        if position in wireApoints:
            continue
        wireApoints[position] = steps + 1

    minIntersectionDistance = sys.maxsize
    for steps, position in enumerate(getWirePoints(wireB)):
        if position in wireApoints:
            minIntersectionDistance = min(minIntersectionDistance, wireApoints[position] + steps + 1)
    
    return minIntersectionDistance


lineRegex = re.compile(r"(?P<direction>R|U|L|D)(?P<distance>\d+)")
def parseLine(line):
    return [ (match.group("direction"), int(match.group("distance"))) for match in lineRegex.finditer(line) ]


def getInput(filePath):
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