#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List


def part1(depths: List[int]) -> int:
    increments = 0
    last_depth = sys.maxsize
    for depth in depths:
        increments += depth > last_depth
        last_depth = depth
    return increments


def part2(depths: List[int]) -> int:
    increments = 0
    last_depth = sys.maxsize
    for index in range(len(depths) - 2):
        depth = sum(depths[index:index + 3])
        increments += depth > last_depth
        last_depth = depth
    return increments


def solve(puzzle_input: str) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ int(line) for line in file.readlines() ]
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
