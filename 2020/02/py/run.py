#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple
import re

Line = Tuple[int,int,str,str]


def count_valid(lines: List[Line], validation_func: Callable[[Line],bool]) -> int:
    return len(list(filter(validation_func, lines)))


def is_line_valid1(line: Line) -> bool:
    minimum, maximum, letter, password = line
    occurence_count = password.count(letter) 
    return occurence_count >= minimum and occurence_count <= maximum


def is_line_valid2(line: Line) -> bool:
    first, second, letter, password = line 
    return (password[first - 1] == letter) ^ (password[second - 1] == letter)


def solve(lines: List[Line]) -> Tuple[int,int]:
    return (
        count_valid(lines, is_line_valid1),
        count_valid(lines, is_line_valid2)
    )


line_regex = re.compile(r"^(\d+)-(\d+)\s([a-z]):\s(.*)$")
def parse_line(line: str) -> Line:
    match = line_regex.match(line)
    if match:
        min, max, letter, password = match.group(1, 2, 3, 4)
        return (int(min), int(max), letter, password)
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Line]:
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