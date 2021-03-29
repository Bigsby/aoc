#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


def part1(steps: int) -> int:
    spin_lock = [0]
    position = 0
    for number in range(1, 2017 + 1):
        position = (position + steps) % len(spin_lock) + 1
        spin_lock.insert(position, number)
    return spin_lock[position + 1]


def part2(steps: int) -> int:
    position = 0
    result = 0
    for number in range(1, 5 * 10 ** 7 + 1):
        position = ((position + steps) % number) + 1
        if (position == 1):
            result = number
    return result


def solve(steps: int) -> Tuple[int, int]:
    return (
        part1(steps),
        part2(steps)
    )


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return int(file.read().strip())


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
