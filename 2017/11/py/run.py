#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


def get_hex_manhatan_distance(position: complex) -> int:
    if (position.real > 0) ^ (position.imag > 0):
        return int(max(abs(position.real), abs(position.imag)))
    return int(abs(position.real) + abs(position.imag))


DIRECTIONS = {
    "s":        1j,
    "se":   1,
    "sw": - 1 + 1j,
    "ne":   1 - 1j,
    "nw": - 1,
    "n":      - 1j
}


def solve(instructions: List[str]) -> Tuple[int, int]:
    furthest = 0
    current_hex = 0
    for instrucion in instructions:
        current_hex += DIRECTIONS[instrucion]
        furthest = max(furthest, get_hex_manhatan_distance(current_hex))
    return get_hex_manhatan_distance(current_hex), furthest


instruction_regex = re.compile(r"ne|nw|n|sw|se|s")


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [match.group() for match in instruction_regex.finditer(file.read())]


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
