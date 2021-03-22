#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


class Disc():
    def __init__(self, positions: int, start: int, index: int):
        self.positions = positions
        self.offset = start + index + 1


def find_winning_position(discs: List[Disc]) -> int:
    jump = 1
    offset = 0
    for disc in discs:
        while (offset + disc.offset) % disc.positions:
            offset += jump
        jump *= disc.positions
    return offset


def solve(discs: List[Disc]) -> Tuple[int, int]:
    part1_result = find_winning_position(discs)
    discs.append(Disc(11, 0, len(discs)))
    return (
        part1_result,
        find_winning_position(discs)
    )


line_regex = re.compile(
    r"^Disc #\d has (?P<positions>\d+) positions; at time=0, it is at position (?P<start>\d+).$")


def parse_line(line: str, index: int) -> Disc:
    match = line_regex.match(line)
    if match:
        positions = int(match.group("positions"))
        start = int(match.group("start"))
        return Disc(positions, start, index)
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Disc]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line, index) for index, line in enumerate(file.readlines())]


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
