#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from itertools import combinations


TARGET_TOTAL = 150


def get_valid_combinations(containers: List[int]) -> List[Tuple[int, ...]]:
    valid_combinations: List[Tuple[int, ...]] = []
    for container_count in range(2, len(containers)):
        for combination in combinations(containers, container_count):
            if sum(combination) == TARGET_TOTAL:
                valid_combinations.append(combination)
    return valid_combinations


def solve(containers: List[int]) -> Tuple[int, int]:
    valid_combinations = get_valid_combinations(containers)
    min_count = min([len(combination) for combination in valid_combinations])
    return \
        len(valid_combinations), \
        len([combination for combination in valid_combinations if len(
            combination) == min_count])


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
