#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Tuple
import re
from itertools import product
from heapq import heappop, heappush

Coordinate = complex
GEOLOGIC_X_CONSTANT = 16807
GEOLOGIC_Y_CONSTANT = 48271
EROSION_CONSTANT = 20183


def get_geologic_index(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate, int]) -> int:
    if coordinate == 0 or coordinate == target:
        return 0
    x, y = int(coordinate.real), int(coordinate.imag)
    if x == 0:
        return y * GEOLOGIC_Y_CONSTANT
    elif y == 0:
        return x * GEOLOGIC_X_CONSTANT
    return get_erosion_level(x - 1 + y * 1j, depth, target, calculated) \
        * get_erosion_level(x + (y - 1) * 1j, depth, target, calculated)


def get_erosion_level(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate, int]) -> int:
    if coordinate not in calculated:
        new_value = (get_geologic_index(
            coordinate, depth, target, calculated) + depth) % EROSION_CONSTANT
        calculated[coordinate] = new_value
    return calculated[coordinate]


def get_risk(coordinate: Coordinate, depth: int, target: Coordinate, calculated: Dict[Coordinate, int]) -> int:
    return get_erosion_level(coordinate, depth, target, calculated) % 3


def part1(data: Tuple[int, ...]) -> int:
    depth, target_x, target_y = data
    target = target_x + target_y * 1j
    calculated: Dict[Coordinate, int] = {}
    return sum(get_risk(x + y * 1j, depth, target, calculated)
               for x, y in product(range(target_x + 1), range(target_y + 1)))


DIRECTIONS = [1, 1j, -1, -1j]


def part2(data: Tuple[int, ...]) -> int:
    depth, x, y = data
    target = x + y * 1j
    calculated: Dict[Coordinate, int] = {}
    final = (x, y, 1)
    queue = [(0, 0, 0, 1)]  # 1 = torch, 0 neither, 2 climbing
    best_times: Dict[Tuple[int, int, int], int] = dict()
    while queue:
        duration, x, y, risk = heappop(queue)
        coordinate = x + y * 1j
        state = (x, y, risk)
        if state in best_times and best_times[state] <= duration:
            continue
        if state == final:
            return duration
        best_times[state] = duration
        for tool in range(3):
            if tool != risk and tool != get_risk(coordinate, depth, target, calculated):
                heappush(queue, (duration + 7, x, y, tool))
        for direction in DIRECTIONS:
            new_coordinate = coordinate + direction
            if new_coordinate.real >= 0 and new_coordinate.imag >= 0 \
                    and get_risk(new_coordinate, depth, target, calculated) != risk:
                heappush(queue, (duration + 1, int(new_coordinate.real),
                                 int(new_coordinate.imag), risk))
    raise Exception("Path not found")


def solve(data: Tuple[int, ...]) -> Tuple[int, int]:
    return (
        part1(data),
        part2(data)
    )


def get_input(file_path: str) -> Tuple[int, ...]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return tuple(map(int, re.findall(r"\d+", file.read())))


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
