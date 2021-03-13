#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from functools import reduce


def part1(adapters: List[int]) -> int:
    diff1 = 0
    diff3 = 1
    current_joltage = 0
    for joltage in adapters:
        diff = joltage - current_joltage
        if diff == 1:
            diff1 += 1
        elif diff == 3:
            diff3 += 1
        current_joltage = joltage
    return diff1 * diff3


def calculate_combinations(sequence: int) -> int:
    if sequence < 3:
        return 1
    if sequence == 3:
        return 2
    return calculate_combinations(sequence - 1) \
        + calculate_combinations(sequence - 2) \
        + calculate_combinations(sequence - 3)


def part2(adapters: List[int]) -> int:
    adapters.append(adapters[-1])
    sequences: List[int] = []
    current_sequence_length = 1
    current_joltage = 0
    for joltage in adapters:
        if current_joltage == joltage - 1:
            current_sequence_length += 1
        else:
            sequences.append(current_sequence_length)
            current_sequence_length = 1
        current_joltage = joltage
    return reduce(lambda soFar, length: soFar * calculate_combinations(length), sequences, 1)


def solve(adapters: List[int]) -> Tuple[int, int]:
    return (
        part1(adapters),
        part2(adapters)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return sorted([int(line) for line in file.readlines()])


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
