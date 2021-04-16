#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from functools import reduce
from itertools import combinations


def get_minimum_group_entanglement(weights: List[int], group_count: int) -> int:
    group_weight = sum(weights) // group_count
    for size in range(1, len(weights)):
        entanglements = [reduce(lambda soFar, weight: soFar * weight, group)
                         for group in combinations(weights, size) if sum(group) == group_weight]
        if entanglements:
            return min(entanglements)
    raise Exception("Group not found")


def solve(weights: List[int]) -> Tuple[int, int]:
    return (
        get_minimum_group_entanglement(weights, 3),
        get_minimum_group_entanglement(weights, 4)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [int(line.strip()) for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
