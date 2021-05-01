#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple
import itertools

DIVISORS = [2, 3, 5, 7, 11, 13]


def sum_powers(powers: Tuple[int]) -> int:
    total = 1
    for k, j in zip(powers, DIVISORS):
        total *= j ** k
    return total


MAX_POWERS = [7, 5, 3, 3,  3,  3]


def get_house(target: int, multiplier: int, limit: int) -> int:
    minimum_house = sys.maxsize
    for powers in itertools.product(*[range(i) for i in MAX_POWERS]):
        total = 0
        elf = sum_powers(powers)
        for j in itertools.product(*[range(k + 1) for k in powers]):
            elf_count = sum_powers(j)
            if elf // elf_count <= limit:
                total += elf_count
        if total * multiplier >= target and elf < minimum_house:
            minimum_house = elf
    return minimum_house


def solve(puzzle_input: int) -> Tuple[int, int]:
    return (
        get_house(puzzle_input, 10, sys.maxsize),
        get_house(puzzle_input, 11, 50)
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
