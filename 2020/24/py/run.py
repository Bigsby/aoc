#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re

Directions = List[str]
Tile = complex
Floor = Dict[Tile, bool]
DIRECTIONS = {
    "e":   1,
    "se":      1j,
    "sw": -1 + 1j,
    "w": -1,
    "ne":  1 - 1j,
    "nw": - 1j
}


def flip_initial_tiles(tile_paths: List[Directions]) -> Floor:
    floor: Floor = {}
    for path in tile_paths:
        current = 0
        for direction in path:
            current += DIRECTIONS[direction]
        if current in floor:
            floor[current] = not floor[current]
        else:
            floor[current] = True
    return floor


def get_neighbors(tile: Tile) -> List[Tile]:
    return [tile + direction for direction in DIRECTIONS.values()]


def get_black_count(neighbors: List[Tile], floor: Floor) -> int:
    return sum([1 for neighbor in neighbors if neighbor in floor and floor[neighbor]])


def get_tile_state(tile: Tile, floor: Floor) -> bool:
    return tile in floor and floor[tile]


def get_new_state(tile: Tile, floor: Floor) -> bool:
    adjacent_black_count = get_black_count(get_neighbors(tile), floor)
    tile_state = get_tile_state(tile, floor)
    if tile_state and adjacent_black_count == 0 or adjacent_black_count > 2:
        return False
    return (not tile_state and adjacent_black_count == 2) or tile_state


def run_day(floor: Floor) -> Floor:
    new_floor: Floor = {}
    edges_to_test: Set[Tile] = set()
    for tile in floor:
        edges_to_test.update(
            {neighbor for neighbor in get_neighbors(tile) if neighbor not in floor})
        new_floor[tile] = get_new_state(tile, floor)
    for tile in edges_to_test:
        new_floor[tile] = get_new_state(tile, floor)
    return new_floor


def part2(floor: Floor) -> int:
    for _ in range(100):
        floor = run_day(floor)
    return sum(floor.values())


def solve(tile_paths: List[Directions]) -> Tuple[int, int]:
    floor = flip_initial_tiles(tile_paths)
    return (
        sum(floor.values()),
        part2(floor)
    )


line_regex = re.compile(r"e|se|sw|w|nw|ne")


def get_input(file_path: str) -> List[Directions]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [line_regex.findall(line.strip()) for line in file.readlines()]


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
