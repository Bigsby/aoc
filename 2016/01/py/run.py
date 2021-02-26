#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Instruction = Tuple[str,int]


def getNewHeading(currentHeading: complex, direction: str) -> complex:
    return currentHeading * (1 if direction == "L" else -1) * 1j


def getManhatanDistance(position: complex) -> int:
    return int(abs(position.real) + abs(position.imag))


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    currentPosition = 0
    currentHeading = 1j
    part2 = 0
    visitedPositions: List[complex] = [ currentPosition ]
    for direction, distance in instructions:
        currentHeading = getNewHeading(currentHeading, direction)
        for _ in range(1, distance + 1):
            currentPosition += currentHeading
            if part2 == 0:
                if currentPosition in visitedPositions:
                    part2 = getManhatanDistance(currentPosition)
                else:
                    visitedPositions.append(currentPosition)
    return (
        getManhatanDistance(currentPosition), 
        part2
    )


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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()