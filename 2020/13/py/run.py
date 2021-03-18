#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from functools import reduce

Bus = Tuple[int, int]


def part1(puzzle_input: Tuple[int, List[Bus]]) -> int:
    timestamp, busses = puzzle_input
    closest_after = sys.maxsize
    closest_bus = None
    for bus in busses:
        time_after = (timestamp // bus[0] + 1) * bus[0] - timestamp
        if time_after < closest_after:
            closest_after = time_after
            closest_bus = bus
    if closest_bus:
        return closest_after * closest_bus[0]
    raise Exception("Closest bus not found")


def modular_multiplicative_inverse(a: int, b: int) -> int:
    q = a % b
    for i in range(1, b):
        if ((q * i) % b) == 1:
            return i
    return 1


def part2(puzzle_input: Tuple[int, List[Bus]]) -> int:
    _, busses = puzzle_input
    product = reduce(lambda soFar, bus: soFar * bus[0], busses, 1)
    sum = 0
    for bus in busses:
        current_product = product // bus[0]
        sum += ((bus[0] - bus[1]) % bus[0]) * current_product * \
            modular_multiplicative_inverse(current_product, bus[0])
    return sum % product


def solve(puzzle_input: Tuple[int, List[Bus]]) -> Tuple[int, int]:
    return (
        part1(puzzle_input),
        part2(puzzle_input)
    )


def get_input(file_path: str) -> Tuple[int, List[Bus]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        lines = file.readlines()
        return int(lines[0]), [(int(busId), index) for index, busId in enumerate(lines[1].split(",")) if busId != "x"]


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
