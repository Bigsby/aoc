#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def is_position_valid(position: complex, number: int) -> bool:
    x, y = int(position.real), int(position.imag)
    if x < 0 or y < 0:
        return False
    value = x*x + 3*x + 2*x*y + y + y*y + number
    return f"{value:b}".count("1") % 2 == 0


DIRECTIONS = [-1, 1j, -1j, 1]


def solve(number: int) -> Tuple[int, int]:
    start_position = 1 + 1j
    queue: List[Tuple[complex, List[complex]]] = [
        (start_position, [start_position])]
    all_visited = {start_position}
    part1_result = 0
    target = 31 + 39 * 1j
    while queue and part1_result == 0:
        position, visited = queue.pop(0)
        for direction in DIRECTIONS:
            new_position = position + direction
            if new_position == target:
                part1_result = len(visited)
            if new_position not in visited and is_position_valid(new_position, number):
                if len(visited) <= 50:
                    all_visited.add(new_position)
                new_visited = list(visited)
                new_visited.append(new_position)
                queue.append((new_position, new_visited))
    return part1_result, len(all_visited)


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
