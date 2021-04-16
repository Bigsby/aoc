#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
from itertools import permutations

Location = complex
Maze = List[complex]


DIRECTIONS = [-1, -1j, 1, 1j]


def find_paths_from_location(maze: Maze, numbers: Dict[Location, int], start: Location) -> Dict[int, int]:
    visited = {start}
    queue: List[Tuple[complex, int]] = [(start, 0)]
    paths: Dict[int, int] = {}
    while queue:
        position, distance = queue.pop(0)
        for direction in DIRECTIONS:
            new_position = position + direction
            if new_position in maze and new_position not in visited:
                visited.add(new_position)
                if new_position in numbers:
                    paths[numbers[new_position]] = distance + 1
                queue.append((new_position, distance + 1))
    return paths


def get_steps_for_path(path: Iterable[int], paths_from_numbers: Dict[int, Dict[int, int]], return_home: bool) -> int:
    steps = 0
    current = 0
    path_list = list(path)
    while path_list:
        next = path_list.pop(0)
        steps += paths_from_numbers[current][next]
        current = next
    if return_home:
        steps += paths_from_numbers[current][0]
    return steps


def solve(data: Tuple[Maze, Dict[Location, int]]) -> Tuple[int, int]:
    maze, numbers = data
    paths_from_numbers = {number: find_paths_from_location(
        maze, numbers, location) for location, number in numbers.items()}
    numbers_besides_start = [
        number for number in numbers.values() if number != 0]
    path_combinations = list(permutations(
        numbers_besides_start, len(numbers_besides_start)))
    minimum_steps = sys.maxsize
    return_minimum_steps = sys.maxsize
    for combination in path_combinations:
        minimum_steps = min(minimum_steps, get_steps_for_path(
            combination, paths_from_numbers, False))
        return_minimum_steps = min(return_minimum_steps, get_steps_for_path(
            combination, paths_from_numbers, True))
    return minimum_steps, return_minimum_steps


def get_input(file_path: str) -> Tuple[Maze, Dict[Location, int]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        maze: Maze = []
        numbers: Dict[Location, int] = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                location = x + y * 1j
                if c == ".":
                    maze.append(location)
                elif c.isdigit():
                    numbers[location] = int(c)
                    maze.append(location)
        return maze, numbers


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
