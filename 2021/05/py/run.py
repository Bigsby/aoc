#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
import re
from collections import defaultdict

Line = Tuple[int, int, int, int]


def get_covered_points(lines: List[Line], diagonals: bool) -> int:
    diagram = defaultdict(int)
    for line in lines:
        x1, y1, x2, y2 = line
        if x1 == x2:
            for y in range(y1 if y1 < y2 else y2, (y1 if y1 > y2 else y2) + 1):
                diagram[(x1, y)] += 1
        elif y1 == y2:
            for x in range(x1 if x1 < x2 else x2, (x1 if x1 > x2 else x2) + 1):
                diagram[(x, y1)] += 1
        elif diagonals:
            x_direction = 1 if x2 > x1 else -1
            y_direction = 1 if y2 > y1 else -1
            count = abs(x2 - x1) + 1
            for xy in range(count):
                diagram[(x1 + xy * x_direction, y1 + xy * y_direction)] += 1
    return len([value for value in diagram.values() if value > 1])


def solve(puzzle_input: List[Line]) -> Tuple[int,int]:
    return (get_covered_points(puzzle_input, False), get_covered_points(puzzle_input, True))


line_regex = re.compile(r"(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)")
def parse_line(line: str) -> Line:
    match = line_regex.match(line)
    if match:
        return (
            int(match.group("x1")),
            int(match.group("y1")),
            int(match.group("x2")),
            int(match.group("y2"))
        )
    raise Exception(f"Bad line: {line}")


def get_input(file_path: str) -> List[Line]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parse_line(line.strip()) for line in file.readlines() ]


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
