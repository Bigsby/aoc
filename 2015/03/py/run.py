#! /usr/bin/python3

import sys, os, time
from typing import List, Set, Tuple


def process_direction(visited_houses: Set[complex], position: complex, direction: complex):
    position += direction
    visited_houses.add(position)
    return position


def part1(directions: List[complex]):
    visited_houses = set()
    visited_houses.add(0)
    position = 0
    for direction in directions:
        position = process_direction(visited_houses, position, direction)
    return len(visited_houses)


def part2(directions: List[complex]):
    visited_houses = set()
    visited_houses.add(0)
    santa_position = robot_position = 0
    for index, direction in enumerate(directions):
        if index % 2:
            santa_position = process_direction(visited_houses, santa_position, direction)
        else:
            robot_position = process_direction(visited_houses, robot_position, direction)
    return len(visited_houses)


def solve(directions: List[complex]) -> Tuple[int,int]:
    return (part1(directions), part2(directions))


DIRECTIONS = {
    "^": -1j,
    "v": 1j,
    ">": 1,
    "<": -1
}
def get_input(file_path: str) -> List[complex]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ DIRECTIONS[c] for c in file.read().strip() if c in DIRECTIONS ]


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