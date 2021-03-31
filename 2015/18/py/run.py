#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple

Grid = Dict[complex, bool]
NEIGHBOR_DIRECTIONS: List[complex] = [
    - 1 - 1j,
    - 1j,
    + 1 - 1j,
    - 1,
    + 1,
    - 1 + 1j,
    + 1j,
    + 1 + 1j
]


def get_neighbors(position: complex) -> Iterable[complex]:
    for direction in NEIGHBOR_DIRECTIONS:
        yield position + direction


def get_next_state(grid: Grid, always_on: List[complex]) -> Grid:
    new_state: Grid = {}
    for position in grid:
        neighbors_active_count = sum(map(
            lambda neighbor: grid[neighbor] if neighbor in grid else 0, get_neighbors(position)))
        new_state[position] = neighbors_active_count == 2 or neighbors_active_count == 3 \
            if grid[position] else \
            neighbors_active_count == 3
    for position in always_on:
        new_state[position] = True
    return new_state


def run_steps(grid: Grid, always_on: List[complex] = []) -> int:
    for position in always_on:
        grid[position] = True
    for _ in range(100):
        grid = get_next_state(grid, always_on)
    return sum(grid.values())


def solve(grid: Grid) -> Tuple[int, int]:
    side = max(map(lambda key: key.real, grid.keys()))
    return (
        run_steps(grid),
        run_steps(grid, [
            0,
            side * 1j,
            side,
            side * (1 + 1j)
        ])
    )


def get_input(file_path: str) -> Grid:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        grid: Grid = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = c == "#"
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
