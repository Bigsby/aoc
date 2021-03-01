#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Instruction = Tuple[str,int]


def get_new_heading(heading: complex, direction: str) -> complex:
    return heading * (1 if direction == "L" else -1) * 1j


def get_manhatan_distance(position: complex) -> int:
    return int(abs(position.real) + abs(position.imag))


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    position = 0
    heading = 1j
    part2 = 0
    visited: List[complex] = [ position ]
    for direction, distance in instructions:
        heading = get_new_heading(heading, direction)
        for _ in range(distance):
            position += heading
            if part2 == 0:
                if position in visited:
                    part2 = get_manhatan_distance(position)
                else:
                    visited.append(position)
    return (
        get_manhatan_distance(position), 
        part2
    )


instruction_regex = re.compile(r"^(?P<direction>[RL])(?P<distance>\d+),?\s?$")
def parse_instruction(text: str) -> Instruction:
    match = instruction_regex.match(text)
    if match:
        return (match.group("direction"), int(match.group("distance")))
    raise Exception("Bad format", text)


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ parse_instruction(instruction) for instruction in file.read().split(" ") ]


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