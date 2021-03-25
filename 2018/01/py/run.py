#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple


def part2(changes: List[int]) -> int:
    changes_length = len(changes)
    frequency = 0
    previous: Set[int] = set()
    index = 0
    while frequency not in previous:
        previous.add(frequency)
        frequency += changes[index]
        index = (index + 1) % changes_length
    return frequency


def solve(changes: List[int]) -> Tuple[int, int]:
    return (
        sum(changes),
        part2(changes)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(line) for line in file.readlines()]


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
