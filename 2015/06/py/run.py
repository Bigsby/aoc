#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List, Tuple
import re

Instruction = Tuple[str,int,int,int,int]


MATRIX_SIDE = 1000
def runMatrix(updateFuncs: Dict[str,Callable[[int],int]], instructions: List[Instruction]) -> int:
    matrix = { (index // MATRIX_SIDE) % MATRIX_SIDE + (index % MATRIX_SIDE) * MATRIX_SIDE: 0 for index in range(MATRIX_SIDE * MATRIX_SIDE) }
    for action, xstart, ystart, xend, yend in instructions:
        updateFunc = updateFuncs[action]
        for x in range(xstart, xend + 1):
            for y in range(ystart, yend + 1):
                position = x + y * MATRIX_SIDE
                matrix[position] = updateFunc(matrix[position])
    return sum(matrix.values())


matrix1Updates: Dict[str,Callable[[int],int]] = {
    "turn on": lambda _: 1,
    "toggle": lambda value: not value,
    "turn off": lambda _: 0
}
matrix2Updates: Dict[str,Callable[[int],int]] = {
    "turn on": lambda value: value + 1,
    "toggle": lambda value: value + 2,
    "turn off": lambda value: value - 1 if value > 0 else 0
}


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (runMatrix(matrix1Updates, instructions), runMatrix(matrix2Updates, instructions))


instructionRegex = re.compile(r"^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$")
def parseLine(line: str) -> Instruction:
    match = instructionRegex.match(line)
    if match:
        return (match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)))
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