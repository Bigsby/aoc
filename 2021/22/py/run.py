#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
import re

Ranges = List[Tuple[int, int]]
Instruction = Tuple[bool, Ranges]
Input = List[Instruction]


def subtract(initial: Ranges, limits: Ranges) -> Ranges:
    result = [(0, 0)] * 3
    for dimension in range(len(result)):
        (limit_start, limit_end) = limits[dimension]
        (start, end) = initial[dimension]
        start = max(start, limit_start)
        end = min(end, limit_end)
        if start < end:
            result[dimension] = (start, end) 
    return result


def is_empty(ranges: Ranges) -> bool:
    return ranges[0] == (0, 0) or ranges[1] == (0, 0) or ranges[2] == (0, 0)


class Cube:
    def __init__(self, ranges: Ranges) -> None:
        self.ranges = ranges
        self.inner_cubes: List[Cube] = []


    def exclude(self, ranges: Ranges) -> None:
        excluded = subtract(ranges, self.ranges)
        if is_empty(excluded):
            return
        for inner_cube in self.inner_cubes:
            inner_cube.exclude(excluded)
        self.inner_cubes.append(Cube(excluded))


    def get_volume(self) -> int:
        result = 1
        for (start, end) in self.ranges:
            result *= end - start
        return result - sum(inner_cube.get_volume() for inner_cube in self.inner_cubes)


def get_on_count(instructions: Input, limits: Ranges) -> int:
    result = 0
    cubes: List[Cube] = []
    for (turn_on, ranges) in instructions:
        if limits:
            ranges = subtract(ranges, limits)
        if is_empty(ranges):
            continue
        cube = Cube(ranges)
        for previous_cube in cubes:
            previous_cube.exclude(ranges)
        if turn_on:
            cubes.append(cube)
    return sum(cube.get_volume() for cube in cubes)


def solve(instructions: Input) -> Tuple[int,int]:
    return (get_on_count(instructions, ((-50, 51), (-50, 51), (-50, 51))), get_on_count(instructions, None))


line_regex = re.compile(r"(?P<turn>on|off) x=(?P<x1>-?\d+)..(?P<x2>-?\d+),y=(?P<y1>-?\d+)..(?P<y2>-?\d+),z=(?P<z1>-?\d+)..(?P<z2>-?\d+)")
def parse_line(line: str) -> Instruction:
    line_match = line_regex.match(line)
    if line_match:
        return (
            line_match.group("turn") == "on",
            [
                (int(line_match.group("x1")), int(line_match.group("x2")) + 1),
                (int(line_match.group("y1")), int(line_match.group("y2")) + 1),
                (int(line_match.group("z1")), int(line_match.group("z2")) + 1)
            ]
        )


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
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
