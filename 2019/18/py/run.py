#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, FrozenSet, List, Set, Tuple
from collections import defaultdict
from heapq import heappop, heappush

Position = complex
Maze = List[Position]
KeysDoors = Dict[Position, str]


def show_maze(maze: Maze, keys_doors: KeysDoors, starts: List[Position]):
    max_x = int(max(p.real for p in maze))
    max_y = int(max(p.imag for p in maze))
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            c = "."
            current = x + y * 1j
            if current in maze:
                c = "#"
            if current in keys_doors:
                c = keys_doors[current]
            if current in starts:
                c = "@"
            print(c, end="")
        print()
    print()


DIRECTIONS = [-1, -1j, 1, 1j]


def find_paths_from_position(maze: Maze, keys_doors: KeysDoors, start: Position) -> Dict[str, Tuple[int, Set[str]]]:
    visited = {start}
    queue: List[Tuple[Position, int, Set[str]]] = [(start, 0, set())]
    paths: Dict[str, Tuple[int, Set[str]]] = {}
    while queue:
        position, distance, required_keys = queue.pop(0)
        for direciton in DIRECTIONS:
            new_position = position + direciton
            if new_position not in maze and new_position not in visited:
                visited.add(new_position)
                new_required_keys = set(required_keys)
                if new_position in keys_doors:
                    key_door = keys_doors[new_position]
                    if key_door.islower():
                        paths[key_door] = distance + 1, required_keys
                    else:
                        new_required_keys.add(key_door.lower())
                queue.append((new_position, distance + 1, new_required_keys))
    return paths


def find_shortest_path_from_key_gragph(
        paths_from_keys: Dict[str, Dict[str, Tuple[int, Set[str]]]],
        keys: Dict[str, Position],
        entrances: List[str]) -> int:
    paths: List[Tuple[int, Tuple[str, ...], FrozenSet[str]]] = [
        (0, tuple(entrances), frozenset())]
    visited: Dict[Tuple[Tuple[str, ...], FrozenSet[str]],
                  int] = defaultdict(int)
    while paths:
        distance, current_points, keys_found = heappop(paths)
        if len(keys_found) == len(keys.keys()):
            return distance
        for current_index, current_key in enumerate(current_points):
            for next_key, next_path in paths_from_keys[current_key].items():
                if next_key not in keys_found:
                    next_keys = frozenset(keys_found | {next_key})
                    next_positions = current_points[:current_index] + \
                        (next_key,) + current_points[current_index + 1:]
                    node_id = (next_positions, next_keys)
                    new_distance = distance + next_path[0]
                    if (node_id not in visited or visited[node_id] > new_distance) and len(next_path[1] - keys_found) == 0:
                        heappush(
                            paths, (new_distance, next_positions, next_keys))
                        visited[node_id] = new_distance
    raise Exception("Path not found")


def find_shortest_path(maze: Maze, keys_doors: KeysDoors, entrances: List[Position]) -> int:
    keys = {key_door: position for position,
            key_door in keys_doors.items() if key_door.islower()}
    keys_paths = {key: find_paths_from_position(
        maze, keys_doors, position) for key, position in keys.items()}
    for index, position in enumerate(entrances):
        keys_paths[str(index)] = find_paths_from_position(
            maze, keys_doors, position)
    return find_shortest_path_from_key_gragph(keys_paths, keys, [str(index) for index, _ in enumerate(entrances)])


def solve(data: Tuple[Maze, KeysDoors, Position]) -> Tuple[int, int]:
    maze, keys_doors, start = data
    part1_result = find_shortest_path(maze, keys_doors, [start])
    for offset in [-1, -1j, 0, 1, 1j]:
        maze.append(start + offset)
    entrances = [
        start + offset for offset in [-1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j]]
    return (
        part1_result,
        find_shortest_path(maze, keys_doors, entrances)
    )


def get_input(file_path: str) -> Tuple[Maze, KeysDoors, Position]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        maze: Maze = []
        keys_doors: KeysDoors = {}
        entrance = 0j
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                position = x + y * 1j
                if c == "#":
                    maze.append(position)
                elif c == "@":
                    entrance = position
                elif c != ".":
                    keys_doors[position] = c
        return maze, keys_doors, entrance


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
