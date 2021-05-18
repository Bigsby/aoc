#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from functools import reduce

Trees = List[complex]


def calculate_trees(trees: Trees, step: complex) -> int:
    y_limit = max(p.imag for p in trees) + 1
    x_limit = max(p.real for p in trees) + 1
    position = 0j
    tree_count = 0
    while position.imag < y_limit:
        tree_count += (position.real % x_limit) + position.imag * 1j in trees
        position += step
    return tree_count


STEPS = [
    1 + 1j,
    3 + 1j,
    5 + 1j,
    7 + 1j,
    1 + 2j
]


def solve(trees: Trees) -> Tuple[int, int]:
    return (
        calculate_trees(trees, 3 + 1j),
        int(reduce(lambda current, step: current *
               calculate_trees(trees, step), STEPS, 1))
    )


def get_input(file_path: str) -> Trees:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        trees: List[complex] = []
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                if c == '#':
                    trees.append(x + y * 1j)
    return trees


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
