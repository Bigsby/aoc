#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Tuple

Grid = Dict[complex, int]
Open, Tree, Lumberyard = 0, 1, 2
RESOURCES = {
    ".": Open,
    "|": Tree,
    "#": Lumberyard
}


NEIGHBOR_DIRECTIONS = [-1 - 1j, -1j, +1 - 1j, -1, +1, -1 + 1j, +1j, 1 + 1j]


def get_count_around(position: complex, grid: Grid, state: int) -> int:
    return sum([1 for direction in NEIGHBOR_DIRECTIONS
                if position + direction in grid and grid[position + direction] == state])


def get_next_minute(grid: Grid) -> Grid:
    new_state: Grid = {}
    for position, state in grid.items():
        if state == Open:
            new_state[position] = Tree if get_count_around(
                position, grid, Tree) > 2 else Open
        elif state == Tree:
            new_state[position] = Lumberyard if get_count_around(
                position, grid, Lumberyard) > 2 else Tree
        elif state == Lumberyard:
            new_state[position] = Lumberyard if get_count_around(
                position, grid, Lumberyard) > 0 and get_count_around(position, grid, Tree) > 0 else Open
    return new_state


def get_resource_value(grid: Grid) -> int:
    return sum([1 for v in grid.values() if v == Tree]) * sum([1 for v in grid.values() if v == Lumberyard])


def solve(grid: Grid) -> Tuple[int, int]:
    previous_values = [grid]
    total = 10 ** 9
    minute = 0
    part1_result = 0
    repeat_found = False
    while minute < total:
        if minute == 10:
            part1_result = get_resource_value(grid)
        minute += 1
        grid = get_next_minute(grid)
        if not repeat_found and grid in previous_values:
            repeat_found = True
            period = minute - previous_values.index(grid)
            minute += ((total - minute) // period) * period
        previous_values.append(grid)
    return part1_result, get_resource_value(grid)


def get_input(file_path: str) -> Grid:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        grid: Grid = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = RESOURCES[c]
        return grid


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
