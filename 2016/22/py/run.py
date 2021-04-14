#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re

FileSystem = Dict[complex, Tuple[int, int]]


def get_empty_and_non_viable_nodes(file_system: FileSystem) -> Tuple[complex, List[complex]]:
    node_names = file_system.keys()
    empty = -0j
    non_viable_nodes: Set[complex] = set()
    for this_node in node_names:
        this_used = file_system[this_node][1]
        if this_used == 0:
            empty = this_node
            continue
        for other_node in node_names:
            if other_node == this_node:
                continue
            if this_used > file_system[other_node][0]:
                non_viable_nodes.add(this_node)
    return empty, list(non_viable_nodes)


DIRECTIONS = [-1j, -1, 1, 1j]


def get_steps_to_target(nodes: List[complex], non_viable: List[complex], start: complex, destination: complex) -> int:
    visited = [start]
    queue: List[Tuple[complex, int]] = [(start, 0)]
    while queue:
        current_node, length = queue.pop(0)
        for direction in DIRECTIONS:
            new_node = current_node + direction
            if new_node == destination:
                return length + 1
            if new_node in nodes and new_node not in visited and new_node not in non_viable:
                visited.append(new_node)
                queue.append((new_node, length + 1))
    raise Exception("Path not found")


def solve(file_system: FileSystem) -> Tuple[int, int]:
    empty, non_viable = get_empty_and_non_viable_nodes(file_system)
    nodes = list(file_system.keys())
    empty_destination = int(max(n.real for n in nodes))
    return (
        len(file_system) - len(non_viable) - 1,
        get_steps_to_target(nodes, non_viable, empty,
                         empty_destination) + (empty_destination - 1) * 5
    )


line_regex = re.compile(
    r"^/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)")


def get_input(file_path: str) -> FileSystem:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        file_system: FileSystem = {}
        for line in file.readlines():
            match = line_regex.match(line)
            if match:
                file_system[int(match.group("x")) + int(match.group("y")) * 1j] = \
                    (int(match.group("size")), int(match.group("used")))
        return file_system


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
