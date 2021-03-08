#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Node = Tuple[List['Node'], List[int]]


def read_node(data: List[int]) -> Node:
    children_count = data.pop()
    metadata_count = data.pop()
    children: List[Node] = []
    metatdata: List[int] = []
    for _ in range(children_count):
        children.append(read_node(data))
    for _ in range(metadata_count):
        metatdata.append(data.pop())
    return children, metatdata


def get_metadata_sum(node: Node) -> int:
    return sum(node[1]) + sum(map(lambda child: get_metadata_sum(child), node[0]))


def get_value(node: Node) -> int:
    children_count = len(node[0])
    if children_count == 0:
        return sum(node[1])
    return sum(map(lambda index: get_value(node[0][index - 1]) if index > 0 and index <= children_count else 0, node[1]))


def solve(data: List[int]) -> Tuple[int, int]:
    data = list(data)
    data.reverse()
    root = read_node(data)
    return (
        get_metadata_sum(root),
        get_value(root)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(i) for i in file.read().strip().split(" ")]


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
