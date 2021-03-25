#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple
import re


class Edge():
    def __init__(self, node_a: str, node_b: str, distance: str):
        self.node_a = node_a
        self.node_b = node_b
        self.distance = int(distance)


def get_single_nodes(edges: List[Edge]) -> List[str]:
    nodes: Set[str] = set()
    for path in edges:
        nodes.add(path.node_a)
        nodes.add(path.node_b)
    return list(nodes)


def get_best_path(edges: List[Edge], longest: bool) -> int:
    single_nodes = get_single_nodes(edges)
    length = len(single_nodes)
    stack: List[Tuple[List[str], str, int]] = [
        ([node], node, 0) for node in single_nodes]
    best_distance = 0 if longest else sys.maxsize
    while stack:
        path, current, distance = stack.pop()
        for edge in filter(lambda edge: edge.node_a == current or edge.node_b == current, edges):
            next_node = edge.node_b if current == edge.node_a else edge.node_a
            if next_node in path:
                continue
            new_distance = distance + edge.distance
            if not longest and new_distance > best_distance:
                continue
            new_path = list(path)
            new_path.append(next_node)
            if len(new_path) == length:
                best_distance = max(best_distance, new_distance) if longest else min(
                    best_distance, new_distance)
            else:
                stack.append((new_path, next_node, new_distance))
    return best_distance


def solve(edges: List[Edge]) -> Tuple[int, int]:
    return (get_best_path(edges, False), get_best_path(edges, True))


line_regex = re.compile(r"^(.*)\sto\s(.*)\s=\s(\d+)$")


def parse_line(line: str) -> Edge:
    match = line_regex.match(line)
    if match:
        return Edge(match.group(1), match.group(2), match.group(3))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Edge]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


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
