#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple

Point = Tuple[int, ...]


def solve(points: List[Point]) -> Tuple[int, str]:
    edges: List[Set[int]] = [set() for _ in range(len(points))]
    for this_point, (w0, x0, y0, z0) in enumerate(points):
        for that_point, (w1, x1, y1, z1) in enumerate(points):
            if abs(w0 - w1) + abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1) < 4:
                edges[this_point].add(that_point)
    visited: Set[int] = set()
    constellations = 0
    for this_point in range(len(points)):
        if this_point in visited:
            continue
        constellations += 1
        queue = [this_point]
        while queue:
            current_point = queue.pop(0)
            if current_point in visited:
                continue
            visited.add(current_point)
            for other in edges[current_point]:
                queue.append(other)
    return constellations, ""


def get_input(file_path: str) -> List[Point]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        points: List[Point] = []
        for line in file.readlines():
            points.append(tuple(map(int, line.strip().split(","))))
        return points


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
