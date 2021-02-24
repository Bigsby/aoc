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


def part1(instructions: List[Instruction]) -> int:
    return navigate(instructions, 1 + 0j)
    

def part2(instructions: List[Instruction]) -> int:
    return navigate(instructions, 10 + 1j, True)


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

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()