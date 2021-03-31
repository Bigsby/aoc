#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Tiles = List[bool]


def solve(tiles: Tiles) -> Tuple[int, int]:
    safe = sum(tiles)
    part1_result = 0
    for step in range(1, 400_000):
        if step == 40:
            part1_result = safe
        tiles = [True] + tiles + [True]
        tiles = [left == right for left, right in zip(tiles, tiles[2:])]
        safe += sum(tiles)
    return part1_result, safe


def get_input(file_path: str) -> Tiles:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return list(c == "." for c in file.read().strip())


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
