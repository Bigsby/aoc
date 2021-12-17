#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict, Iterable
from collections import defaultdict
from heapq import heappop, heappush

Position = Tuple[int, int]
Input = Tuple[Dict[Position, int], int, int]


def get_neighbors(position: Position, width: int, height: int) -> Iterable[Position]:
    x, y = position
    if x:
        yield (x - 1, y)
    if y:
        yield (x, y - 1)
    if x < width - 1:
        yield (x + 1, y)
    if y < height - 1:
        yield (x, y + 1)


def get_position_risk(
    risk_levels: Dict[Position, int], position: Position, width: int, height: int
) -> int:
    x, y = position
    risk = risk_levels[(x % width, y % height)] + x // width + y // height
    return risk if risk < 10 else risk - 9


def get_lowest_risk(puzzle_input: Input, expansion: int) -> int:
    risk_levels, width, height = puzzle_input
    expanded_width = width * expansion
    expanded_height = height * expansion
    target = (expanded_width - 1, expanded_height - 1)
    distances: Dict[Position, int] = defaultdict(lambda: sys.maxsize)
    distances[(0, 0)] = 0
    to_check = [(0, (0, 0))]
    while True:
        current_risk, current = heappop(to_check)
        if current == target:
            return current_risk
        for neighbor in get_neighbors(current, expanded_width, expanded_height):
            new_neighbor_risk_level = current_risk + get_position_risk(
                risk_levels, neighbor, width, height
            )
            if distances[neighbor] > new_neighbor_risk_level:
                distances[neighbor] = new_neighbor_risk_level
                heappush(to_check, (new_neighbor_risk_level, neighbor))


def solve(puzzle_input: Input) -> Tuple[int, int]:
    return (get_lowest_risk(puzzle_input, 1), get_lowest_risk(puzzle_input, 5))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        cavern: Dict[Position, int] = dict()
        y = 0
        x = 0
        for line in file.readlines():
            x = 0
            for c in line.strip():
                cavern[(x, y)] = int(c)
                x += 1
            y += 1
        return cavern, x, y


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
