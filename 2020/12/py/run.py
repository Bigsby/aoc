#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


Instruction = Tuple[str,int]
CARDINAL_DIRECTIONS = {
    "N": 1j, 
    "S": -1j, 
    "E": 1, 
    "W": -1
}
ROTATIONS = {
    "L": 1j, 
    "R": -1j
}


def navigate(instructions: List[Instruction], heading: complex,  headingOnCardinal: bool = False) -> int:
    position = 0j
    for direction, value in instructions:
        if direction in CARDINAL_DIRECTIONS:
            if headingOnCardinal:
                heading += CARDINAL_DIRECTIONS[direction] * value
            else:
                position += CARDINAL_DIRECTIONS[direction] * value
        elif direction in ROTATIONS:
            heading *= ROTATIONS[direction] ** (value // 90)
        elif direction == "F":
            position += heading * value
    return int(abs(position.real) + abs(position.imag))


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (
        navigate(instructions, 1 + 0j),
        navigate(instructions, 10 + 1j, True)
    )


lineRegex = re.compile(r"^(?P<direction>[NSEWLRF])(?P<value>\d+)$")
def parseLine(line: str) -> Instruction:
    match = lineRegex.match(line)
    if match:
        return match.group("direction"), int(match.group("value"))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Instruction]:
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