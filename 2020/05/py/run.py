#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def part2(seats: List[int]) -> int:
    last_id = min(seats)
    for current_id in sorted(seats):
        if current_id - last_id == 2:
            return last_id + 1
        last_id = current_id
    raise Exception("Seat not found")


def solve(seats: List[int]) -> Tuple[int, int]:
    return (
        max(seats),
        part2(seats)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2)
                for line in file.readlines()]


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
