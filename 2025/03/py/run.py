#! /usr/bin/python3

import sys, os, time
from itertools import combinations
from functools import reduce
from typing import Tuple, List

Input = List[str]


def max_joltage(bank: str, battery_count) -> int:
    max_selection = ""
    start_index = 0
    while len(max_selection) < battery_count:
        current = "0"
        current_index = 0
        for index in range(start_index, len(bank) - battery_count + len(max_selection) + 1):
            if bank[index] > current:
                current = bank[index]
                current_index = index
        max_selection += current
        start_index = current_index + 1
    return int(max_selection)


def max_joltage_sum(puzzle_input: Input, battery_count: int) -> int:
    return sum(max_joltage(bank, battery_count) for bank in puzzle_input)


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (max_joltage_sum(puzzle_input, 2), max_joltage_sum(puzzle_input, 12))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ line.strip() for line in file.readlines() ]


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
