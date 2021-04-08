#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Range = Tuple[int, int]


def solve(ranges: List[Range]) -> Tuple[int, int]:
    part1_result = 0
    ranges.sort()
    previous_upper = 0
    allowed_count = 0
    for lower, upper in ranges:
        if upper <= previous_upper:
            continue
        if lower > previous_upper + 1:
            allowed_count += lower - previous_upper - 1
            if part1_result == 0:
                part1_result = previous_upper + 1
        previous_upper = upper
    return part1_result, allowed_count


def parse_line(line: str) -> Range:
    splits = line.strip().split("-")
    return int(splits[0]), int(splits[1])


def get_input(file_path: str) -> List[Range]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
