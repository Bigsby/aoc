#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


BASE_SUBJECT_NUMBER = 7
DIVIDER = 20201227


def get_next_value(value: int, subject_number: int = BASE_SUBJECT_NUMBER) -> int:
    return (value * subject_number) % DIVIDER


def get_loop_size(target: int) -> int:
    value = 1
    cycle = 0
    while value != target:
        cycle += 1
        value = get_next_value(value)
    return cycle


def transform(subject_number: int, cycles: int) -> int:
    value = 1
    while cycles:
        cycles -= 1
        value = get_next_value(value, subject_number)
    return value


def solve(puzzle_input: Tuple[int, ...]) -> Tuple[int, str]:
    card, door = puzzle_input
    return transform(card, get_loop_size(door)), ""


def get_input(file_path: str) -> Tuple[int, ...]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return tuple(int(line.strip()) for line in file.readlines())


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
