#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from itertools import product

Grid = List[int]
GRID_SIZE = 300


def get_index(x: int, y: int) -> int:
    return y * GRID_SIZE + x

def calculate_power_level(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = power_level % 1000 // 100
    return power_level - 5


def build_grid(serial_number: int) -> Grid:
    return [calculate_power_level(x + 1, y + 1, serial_number) 
        for y, x in product(range(GRID_SIZE), range(GRID_SIZE))]


def build_summed_area_table(grid: Grid) -> Grid:
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            grid[get_index(x, y)] = \
                  grid[get_index(x    , y    )] + \
                ( grid[get_index(x - 1, y    )] if x > 0 else 0) + \
                ( grid[get_index(x    , y - 1)] if y > 0 else 0) + \
                (-grid[get_index(x - 1, y - 1)] if x > 0 and y > 0 else 0)
    return grid


def sum_from_area_table(grid: Grid, x: int, y: int, size: int) -> int:
    return grid[get_index(x - 1       , y - 1       )] \
         - grid[get_index(x - 1 + size, y - 1       )] \
         - grid[get_index(x - 1       , y - 1 + size)] \
         + grid[get_index(x - 1 + size, y - 1 + size)]


def solve(serial_number: int) -> Tuple[str, str]:
    grid = build_grid(serial_number)
    summed_area_table = build_summed_area_table(grid)
    max_fuel = max_size = 0
    max_cell = (-1, -1)
    max3_cell = (-1, -1)
    max3_fuel = 0
    for size in range(1, GRID_SIZE):
        for y, x in product(range(1, GRID_SIZE - size), range(1, GRID_SIZE - size)):
            fuel = sum_from_area_table(summed_area_table, x, y, size)
            if fuel > max_fuel:
                max_fuel = fuel
                max_cell = x + 1, y + 1
                max_size = size
            if size == 3 and fuel > max3_fuel:
                max3_fuel = fuel
                max3_cell = x + 1, y + 1
    return f"{max3_cell[0]},{max3_cell[1]}", f"{max_cell[0]},{max_cell[1]},{max_size}"


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return int(file.read().strip())


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
