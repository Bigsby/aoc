#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


hexa_regex = re.compile(r"\\x[0-9a-f]{2}")


def get_string_difference_1(string: str) -> int:
    total_length = len(string)
    stripped = string.replace(r"\\", "r").replace(r"\"", "r")
    stripped = hexa_regex.sub("r", stripped)
    return total_length - len(stripped.strip(r"\""))


def get_string_difference_2(string: str) -> int:
    return 2 + len(re.escape(string).replace("\"", "\\\"")) - len(string)


def solve(strings: List[str]) -> Tuple[int, int]:
    return (
        sum(map(get_string_difference_1, strings)),
        sum(map(get_string_difference_2, strings)),
    )


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


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
