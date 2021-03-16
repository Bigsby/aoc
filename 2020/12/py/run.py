#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


Instruction = Tuple[str, int]
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


def navigate(instructions: List[Instruction], heading: complex,  heading_on_cardinal: bool = False) -> int:
    position = 0j
    for direction, value in instructions:
        if direction in CARDINAL_DIRECTIONS:
            if heading_on_cardinal:
                heading += CARDINAL_DIRECTIONS[direction] * value
            else:
                position += CARDINAL_DIRECTIONS[direction] * value
        elif direction in ROTATIONS:
            heading *= ROTATIONS[direction] ** (value // 90)
        elif direction == "F":
            position += heading * value
    return int(abs(position.real) + abs(position.imag))


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    return (
        navigate(instructions, 1 + 0j),
        navigate(instructions, 10 + 1j, True)
    )


line_regex = re.compile(r"^(?P<direction>[NSEWLRF])(?P<value>\d+)$")


def parse_line(line: str) -> Instruction:
    match = line_regex.match(line)
    if match:
        return match.group("direction"), int(match.group("value"))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
