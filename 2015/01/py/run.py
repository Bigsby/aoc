#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def part2(directions: List[int]) -> int:
    current_floor = 0
    for index, direction in enumerate(directions):
        current_floor += direction
        if current_floor == -1:
            return index + 1
    raise Exception("Did not go below 0!")


def solve(directions: List[int]) -> Tuple[int,int]:
    return (sum(directions), part2(directions))


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ 1 if c == "(" else -1 for c in file.read().strip() ]


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