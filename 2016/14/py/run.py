#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re
from hashlib import md5


triplet_regex = re.compile(r"(.)\1{2}")
quintet_regex = re.compile(r"(.)\1{4}")


def find_key(salt: str, stretch: int) -> int:
    index = 0
    keys: List[int] = []
    threes: Dict[str, List[int]] = {digit: [] for digit in "0123456789abcdef"}
    while len(keys) < 64:
        value = salt + str(index)
        for _ in range(stretch + 1):
            value = md5(value.encode()).hexdigest()
        match = quintet_regex.search(value)
        if match:
            digit = match.group()[0]
            for triplet_index in threes[digit]:
                if (index - triplet_index) <= 1000:
                    keys.append(triplet_index)
            threes[digit] = []

        match = triplet_regex.search(value)
        if match:
            threes[match.group()[0]].append(index)
        index += 1
    keys.sort()
    return keys[63]


def solve(salt: str) -> Tuple[int, int]:
    return (
        find_key(salt, 0),
        find_key(salt, 2016)
    )


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
