#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


def part1(dimensions: List[Tuple[int,int,int]]) -> int:
    total_paper = 0
    for w, l, h in dimensions:
        wl = w * l
        wh = w * h
        hl = h * l
        smallest = min(wl, wh, hl)
        total_paper += 2 * (wl + wh + hl) + smallest
    return total_paper


def part2(dimensions: List[Tuple[int,int,int]]) -> int:
    total_ribbon = 0
    for w, l, h in dimensions:
        sides_list = [w, l, h]
        sides_list.sort()
        total_ribbon += 2 * (sides_list[0] + sides_list[1]) + w * l * h
    return total_ribbon


def solve(dimensions: List[Tuple[int,int,int]]) -> Tuple[int,int]:
    return (part1(dimensions), part2(dimensions))


line_regex = re.compile(r"^(\d+)x(\d+)x(\d+)$")
def parse_line(line:str) -> Tuple[int,int,int]:
    match = line_regex.match(line)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Tuple[int,int,int]]:
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