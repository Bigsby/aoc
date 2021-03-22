#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
import re

Wire = List[Tuple[str, int]]
Position = complex


STEPS = {
    "R": 1,
    "U": -1j,
    "L": -1,
    "D": 1j
}


def get_wire_oositions(wire: Wire) -> Iterable[Position]:
    position = 0j
    for direction, distance in wire:
        for _ in range(distance):
            position += STEPS[direction]
            yield position


def part1(wires: Tuple[Wire, Wire]) -> int:
    wire_a, wire_b = wires
    wire_a_points = set(get_wire_oositions(wire_a))
    return int(min([abs(position.real) + abs(position.imag)
                    for position in get_wire_oositions(wire_b)
                    if position in wire_a_points]))


def part2(wires: Tuple[Wire, Wire]) -> int:
    wire_a, wire_b = wires
    wire_a_points: Dict[Position, int] = {}
    for steps, position in enumerate(get_wire_oositions(wire_a)):
        if position not in wire_a_points:
            wire_a_points[position] = steps + 1
    return min([wire_a_points[position] + steps + 1
                for steps, position in enumerate(get_wire_oositions(wire_b))
                if position in wire_a_points])


def solve(wires: Tuple[Wire, Wire]) -> Tuple[int, int]:
    return (
        part1(wires),
        part2(wires)
    )


line_regex = re.compile(r"(?P<direction>R|U|L|D)(?P<distance>\d+)")


def parse_line(line: str) -> Wire:
    return [(match.group("direction"), int(match.group("distance"))) for match in line_regex.finditer(line)]


def get_input(file_path: str) -> Tuple[Wire, Wire]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        lines = file.readlines()
        return parse_line(lines[0]), parse_line(lines[1])


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
