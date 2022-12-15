#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[Tuple[int, int, int, int]]


def get_manhatan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def part1(data: List[Tuple[int, int, int]]) -> int:
    LINE = 2_000_000  # 10 for example input
    return max(x - abs(LINE - y) + distance for x, y, distance in data) - \
        min(x + abs(LINE - y) - distance for x, y, distance in data)


def part2(data: List[Tuple[int, int, int]]) -> int:
    MIN = 0
    MAX = 4_000_000  # 20 for example input
    for xa, ya, da in data:
        for xb, yb, db in data:
            cross_distance_a = xa - ya - da
            cross_distance_b = xb + yb + db
            beacon_x = (cross_distance_b + cross_distance_a) // 2
            beacon_y = (cross_distance_b - cross_distance_a) // 2 + 1
            if MIN < beacon_x < MAX and MIN < beacon_y <= MAX \
                    and all(get_manhatan_distance(beacon_x, beacon_y, x, y) > distance for x, y, distance in data):
                return 4_000_000 * beacon_x + beacon_y
    raise Exception("Beam not found!")


def solve(puzzle_input: Input) -> Tuple[int, int]:
    data: List[Tuple[int, int, int]] = [(sensor_x, sensor_y, get_manhatan_distance(
        sensor_x, sensor_y, beacon_x, beacon_y)) for sensor_x, sensor_y, beacon_x, beacon_y in puzzle_input]
    return (part1(data), part2(data))


def get_value(text: str) -> int:
    return int(text.strip(":,").split('=')[1])


def process_line(line: str) -> Tuple[int, int, int, int]:
    split = line.split()
    return get_value(split[2]), get_value(split[3]), get_value(split[8]), get_value(split[9])


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [process_line(line) for line in file.readlines()]


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
