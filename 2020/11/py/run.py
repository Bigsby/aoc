#! /usr/bin/python3

import sys
import os
import time
from typing import Callable, Dict, Tuple
from enum import Enum


class State(Enum):
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'


Grid = Dict[complex, State]
NeighborFinder = Callable[[Grid, complex, complex], complex]


NEIGHBOR_DIRECTIONS = [
    - 1 - 1j,
        - 1j,
    + 1 - 1j,
    - 1,
    + 1,
    - 1 + 1j,
        + 1j,
    + 1 + 1j
]


def get_occupied_count(grid: Grid, position: complex, get_neighbor_func: NeighborFinder) -> int:
    total = 0
    for direction in NEIGHBOR_DIRECTIONS:
        neighbor = get_neighbor_func(grid, position, direction)
        if neighbor in grid and grid[neighbor] == State.OCCUPIED:
            total += 1
    return total


def get_position_new_state(grid: Grid, position: complex, tolerance: int, get_neighbor_func: NeighborFinder) -> Tuple[bool, State]:
    current_state = grid[position]
    if current_state == State.FLOOR:
        return False, State.FLOOR
    occupied_count = get_occupied_count(grid, position, get_neighbor_func)
    if current_state == State.EMPTY and occupied_count == 0:
        return True, State.OCCUPIED
    if current_state == State.OCCUPIED and occupied_count > tolerance:
        return True, State.EMPTY
    return False, current_state


def get_next_state(grid: Grid, tolerance: int, get_neighbor_func: NeighborFinder) -> Tuple[bool, Grid]:
    new_state = dict(grid)
    any_change = False
    for position in grid:
        changed, new_position_state = get_position_new_state(
            grid, position, tolerance, get_neighbor_func)
        any_change |= changed
        new_state[position] = new_position_state
    return any_change, new_state


def run_grid(grid: Grid, tolerance: int, get_neighbor_func: NeighborFinder) -> int:
    grid = dict(grid)
    changed = True
    count = 0
    while changed:
        count += 1
        changed, grid = get_next_state(grid, tolerance, get_neighbor_func)
    return sum(map(lambda value: 1 if value == State.OCCUPIED else 0, grid.values()))


def get_directional_neighbor(grid: Grid, position: complex, direction: complex) -> complex:
    position += direction
    while position in grid and grid[position] == State.FLOOR:
        position += direction
    return position


def solve(grid: Grid) -> Tuple[int, int]:
    return (
        run_grid(grid, 3, lambda _, position, direction: position + direction),
        run_grid(grid, 4, get_directional_neighbor)
    )


def get_input(file_path: str) -> Grid:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        grid: Grid = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                grid[x + y * 1j] = State(c)
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
