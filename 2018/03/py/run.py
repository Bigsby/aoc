#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from itertools import product

Claim = Tuple[int,int,int,int,int]


def get_covered_points(claims: List[Claim]) -> Dict[Tuple[int,int],int]:
    covered_points: Dict[Tuple[int,int],int] = {}
    for _, left, top, width, height in claims:
        for point in product(range(left, left + width), range(top, top + height)):
            if point in covered_points:
                covered_points[point] += 1
            else:
                covered_points[point] = 1
    return covered_points


def part2(claims: List[Claim], covered_points: Dict[Tuple[int,int],int]) -> int:
    for id, left, top, width, height in claims:
        if all(covered_points[point] == 1 for point in product(range(left, left + width), range(top, top + height))):
            return id
    raise Exception("Claim not found")


def solve(claims: List[Claim]) -> Tuple[int,int]:
    covered_points = get_covered_points(claims)
    return (
        sum([ 1 for value in covered_points.values() if value > 1 ]),
        part2(claims, covered_points)
    )


line_regex = re.compile(r"^#(?P<id>\d+)\s@\s(?P<left>\d+),(?P<top>\d+):\s(?P<width>\d+)x(?P<height>\d+)$")
def parse_line(line: str) -> Claim:
    match = line_regex.match(line)
    if match:
        return (
            int(match.group("id")),
            int(match.group("left")),
            int(match.group("top")),
            int(match.group("width")),
            int(match.group("height"))
        )
    raise Exception("Bad format", line)
    

def get_input(file_path: str) -> List[Claim]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ parse_line(line) for line in file.readlines() ]


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