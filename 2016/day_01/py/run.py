#! /usr/bin/python3

import sys, os, time
from typing import Iterable, List, Tuple
import re

Instruction = Tuple[str,int]


def getNewHeading(currentHeading: complex, direction: str) -> complex:
    return currentHeading * (1 if direction == "L" else -1) * 1j


def getManhatanDistance(position: complex) -> int:
    return int(abs(position.real) + abs(position.imag))


def part1(instructions: List[Instruction]):
    currentPosition = 0
    currentHeading = 1j

    for direction, distance in instructions:
        currentHeading = getNewHeading(currentHeading, direction)
        currentPosition += currentHeading * distance

    return getManhatanDistance(currentPosition)


def getVisitedPositions(position: complex, heading: complex, distance: int) -> Iterable[complex]:
    for i in range(1, distance + 1):
        yield position + (i * heading)


def part2(instructions: List[Instruction]) -> int:
    currentPosition = 0
    currentHeading = 1j
    visitedPositions: List[complex] = [ currentPosition ]

    for direction, distance in instructions:
        currentHeading = getNewHeading(currentHeading, direction)
        for i in range(1, distance + 1):
            currentPosition += currentHeading
            if currentPosition in visitedPositions:
                return getManhatanDistance(currentPosition)
            else:
                visitedPositions.append(currentPosition)
    raise Exception("Never returned to previous locations")


instructionRegex = re.compile(r"^(?P<direction>[RL])(?P<distance>\d+),?\s?$")
def parseInstruction(instructionText: str) -> Instruction:
    match = instructionRegex.match(instructionText)
    if match:
        return (match.group("direction"), int(match.group("distance")))
    raise Exception("Bad format", instructionText)

def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseInstruction(instruction) for instruction in file.read().split(" ") ]


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