#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
from collections import defaultdict


DIRECTIONS = {
    "N": 1j,
    "S": -1j,
    "E": 1,
    "W": -1
}


def get_distances(routes: str) -> Iterable[int]:
    distances: Dict[complex, int] = defaultdict(lambda: sys.maxsize)
    distances[0j] = 0
    group_ends: List[complex] = []
    head = 0j
    for c in routes[1:-1]:
        if c == "(":
            group_ends.append(head)
        elif c == ")":
            head = group_ends.pop()
        elif c == "|":
            head = group_ends[-1]
        else:
            previous = head
            head += DIRECTIONS[c]
            distances[head] = min(distances[head], distances[previous] + 1)
    return distances.values()


def solve(routes: str) -> Tuple[int, int]:
    distances = get_distances(routes)
    return (
        max(distances),
        sum(1 for distance in distances if distance >= 1000)
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
