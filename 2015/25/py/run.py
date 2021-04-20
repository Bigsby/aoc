#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple
import re


FIRST_CODE = 20151125
MULTIPLIER = 252533
DIVIDER = 33554393


def solve(data: Tuple[int, ...]) -> Tuple[int, str]:
    target_row, target_column = data
    last_code = FIRST_CODE
    current_length = 1
    while True:
        column = 0
        current_length += 1
        row = current_length
        while row:
            column += 1
            last_code = (last_code * MULTIPLIER) % DIVIDER
            if column == target_column and row == target_row:
                return (last_code, "")
            row -= 1


def get_input(file_path: str) -> Tuple[int, ...]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return tuple(map(int, re.findall(r"\d+", file.read())))


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
