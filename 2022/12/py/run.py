#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict, List, Set

Input = Tuple[Dict[complex, int], complex, complex]

DIRECTIONS = [-1, -1j, 1, 1j]


def find_shortest_path(heightmap: Dict[complex, int], start: complex, end: complex) -> int:
    visited: Set[complex] = {start}
    queue: List[Tuple[complex, List[complex]]] = [(start, [start])]
    while queue:
        position, path = queue.pop(0)
        for direction in DIRECTIONS:
            new_position = position + direction
            if new_position in visited or new_position not in heightmap or heightmap[new_position] - heightmap[position] > 1:
                continue
            if new_position == end:
                return len(path)
            visited.add(new_position)
            new_path = list(path)
            new_path.append(new_position)
            queue.append((new_position, new_path))
    return sys.maxsize


def part1(puzzle_input: Input) -> int:
    heightmap, start, end = puzzle_input
    return find_shortest_path(heightmap, start, end)


def part2(puzzle_input: Input) -> int:
    heightmap, _, end = puzzle_input
    shortest_path = sys.maxsize
    for position, height in heightmap.items():
        if height == ord('a'):
            shortest_path = min(
                shortest_path, find_shortest_path(heightmap, position, end))
    return shortest_path


def solve(puzzle_input: Input) -> Tuple[int, int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        start = 0j
        end = 0j
        heightmap: Dict[complex, int] = dict()
        position = 0j
        for line in file.readlines():
            for c in line.strip():
                if c == "S":
                    start = position
                    heightmap[position] = ord('a')
                elif c == "E":
                    end = position
                    heightmap[position] = ord('z')
                else:
                    heightmap[position] = ord(c)
                position += 1
            position = (position.imag + 1) * 1j
        return heightmap, start, end


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
