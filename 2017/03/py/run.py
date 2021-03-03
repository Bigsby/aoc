#! /usr/bin/python3

import sys, os, time
from math import floor, sqrt
from typing import Dict, List, Tuple


def part1(target_number: int) -> int:
    side = floor(sqrt(target_number)) + 1
    past_last_square = target_number - (side - 1) ** 2
    half_side = side // 2
    if past_last_square >= side:
        past_last_square -= side
    offset_to_middle = abs(half_side - past_last_square)
    return half_side + offset_to_middle


DIRECTIONS: List[complex] = [
    - 1 - 1j, - 1j, 1 - 1j,
    - 1,            1,
    - 1 + 1j,   1j, 1 + 1j
]
def get_sum_for_neighbors(grid: Dict[complex,int], position:complex) -> int:
    return sum(map(lambda neighbor: grid[neighbor] if neighbor in grid else 0, \
        map(lambda direction: position + direction, DIRECTIONS)))


def part2(target: int) -> int:
    grid: Dict[complex,int] = { 0j: 1 }
    position = 0j
    direction = 1
    moves_in_direction = 1
    while True:
        for _ in range(2):
            direction *= 1j
            for _ in range(moves_in_direction):
                position += direction
                new_value = get_sum_for_neighbors(grid, position)
                if new_value > target:
                    return new_value
                grid[position] = new_value
        moves_in_direction += 1


def solve(target: int) -> Tuple[int,int]:
    return (
        part1(target),
        part2(target)
    )


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return int(file.read())


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