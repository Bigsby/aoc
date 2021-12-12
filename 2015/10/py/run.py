#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def get_next_value(value: str) -> str:
    sequences: List[str] = []
    last_digit = value[0]
    length = 1
    for c in value[1:]:
        if c == last_digit:
            length += 1
        else:
            sequences.append(str(length))
            sequences.append(last_digit)
            last_digit = c
            length = 1
    sequences.append(str(length))
    sequences.append(last_digit)
    return "".join(sequences)


def solve(puzzle_input: str) -> Tuple[int, int]:
    current_value = puzzle_input
    part1 = 0
    for turn in range(50):
        if turn == 40:
            part1 = len(current_value)
        current_value = get_next_value(current_value)
    return (part1, len(current_value))


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


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
