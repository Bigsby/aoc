#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Instruction = List[str]


def solve(instructions: List[Instruction]) -> Tuple[int, str]:
    target = int(instructions[1][1]) * int(instructions[2][1])
    a = 1
    while a < target:
        if a % 2 == 0:
            a = a * 2 + 1
        else:
            a *= 2
    return a - target, ""


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [line.split(" ") for line in file.readlines()]


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
