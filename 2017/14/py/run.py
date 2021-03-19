#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple
from functools import reduce

MARKS_COUNT = 256


def run_lengths(marks: List[int], lengths: List[int], current_mark: int, skip: int) -> Tuple[List[int], int, int]:
    for length in lengths:
        to_reverse: List[int] = []
        reverse_mark = current_mark
        for _ in range(length):
            to_reverse.append(marks[reverse_mark])
            reverse_mark = reverse_mark + 1 if reverse_mark < MARKS_COUNT - 1 else 0
        reverse_mark = current_mark
        for _ in range(length):
            marks[reverse_mark] = to_reverse.pop()
            reverse_mark = reverse_mark + 1 if reverse_mark < MARKS_COUNT - 1 else 0
        for _ in range(length + skip):
            current_mark = current_mark + 1 if current_mark < MARKS_COUNT - 1 else 0
        skip += 1
    return marks, current_mark, skip


SUFFIX = [17, 31, 73, 47, 23]


def knot_hash(key: str) -> str:
    lengths = [ord(c) for c in key]
    lengths.extend(SUFFIX)
    marks = [i for i in range(MARKS_COUNT)]
    current_mark = skip = 0
    for _ in range(64):
        marks, current_mark, skip = run_lengths(
            marks, lengths, current_mark, skip)
    dense_hash = map(lambda index:
                     reduce(lambda soFar, mark: soFar ^ mark, marks[index * 16:(index + 1) * 16]), range(16))
    return "".join(map(lambda knot: f"{knot:02x}", dense_hash))


def get_row_hash_binary_string(key: str, index: int) -> str:
    row_hash = int(knot_hash(key + "-" + str(index)), 16)
    return f"{row_hash:0128b}"


DIRECTIONS = [1j, 1, -1j, -1]


def find_adjacent(point: complex, grid: Set[complex], visited: Set[complex]):
    for direction in DIRECTIONS:
        adjacent = point + direction
        if adjacent in grid and adjacent not in visited:
            visited.add(adjacent)
            find_adjacent(adjacent, grid, visited)


def part2(key: str) -> int:
    grid_points = set()
    for row in range(128):
        for column, c in enumerate(get_row_hash_binary_string(key, row)):
            if c == "1":
                grid_points.add(column + row * 1j)
    regions = 0
    while grid_points:
        regions += 1
        point = grid_points.pop()
        visited = {point}
        find_adjacent(point, grid_points, visited)
        grid_points -= visited
    return regions


def solve(key: str) -> Tuple[int, int]:
    return (
        sum(map(lambda index: get_row_hash_binary_string(
            key, index).count("1"), range(128))),
        part2(key)
    )


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


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
