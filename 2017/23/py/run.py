#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


def part2(number: int) -> int:
    total = number * 100 + 100000
    non_primes = 0
    for candidate in range(total, total + 17000 + 1, 17):
        divider = 2
        while candidate % divider != 0:
            divider += 1
        non_primes += candidate != divider
    return non_primes


def solve(number: int) -> Tuple[int, int]:
    return (
        (number - 2) ** 2,
        part2(number)
    )


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return int(file.readlines()[0].split(" ")[2])


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
