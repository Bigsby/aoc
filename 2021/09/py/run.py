#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict, Iterable

Map = (Dict[complex, int], int, int)

def get_neighbors(puzzle_input: Map, position: complex) -> Iterable[complex]:
    height_map, max_x, max_y = puzzle_input
    if position.real:
        yield position.real - 1 + position.imag * 1j
    if position.imag:
        yield position.real + (position.imag - 1) * 1j
    if position.real < max_x - 1:
        yield position.real + 1 + position.imag * 1j
    if position.imag < max_y - 1:
        yield position.real + (position.imag + 1) * 1j
    

def get_position_risk(puzzle_input: Map, position: complex) -> int:
    height_map, max_x, max_y = puzzle_input
    height = height_map[position]
    for neighbor in get_neighbors(puzzle_input, position):
        if height_map[neighbor] <= height:
            return 0
    return height + 1
    

def get_basin_size(puzzle_input: Map, position: complex) -> int:
    height_map, max_x, max_y = puzzle_input
    to_visit = [position]
    visited = [] 
    while len(to_visit):
        current = to_visit.pop(0)
        if current in visited:
            continue
        current_height = height_map[current]
        visited.append(current)
        for neighbor in get_neighbors(puzzle_input, current):
            neighbor_height = height_map[neighbor]
            if neighbor_height == 9 or neighbor in visited or neighbor_height <= current_height:
                continue
            to_visit.append(neighbor)
    return len(visited)


def solve(puzzle_input: Map) -> Tuple[int,int]:
    _, max_x, max_y = puzzle_input
    lowest_sum = 0
    sizes = []
    for y in range(max_y):
        for x in range(max_x):
            position = x + y * 1j
            position_risk = get_position_risk(puzzle_input, position)
            if position_risk:
                lowest_sum += position_risk
                sizes.append(get_basin_size(puzzle_input, position))
    sizes.sort(reverse=True)
    return lowest_sum, sizes[0] * sizes[1] * sizes[2]


def get_input(file_path: str) -> Map:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        height_map = dict()
        max_x = 0
        max_y = 0
        position = 0j
        for line in file.readlines():
            for height in line:
                if height == "\n":
                    continue
                height_map[position] = int(height)
                position += 1
            max_x = position.real
            position = (position.imag + 1) * 1j
        return height_map, int(max_x), int(position.imag)


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
