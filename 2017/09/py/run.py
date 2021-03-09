#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


GROUP_START = "{"
GROUP_END = "}"
GARBAGE_START = "<"
GARBAGE_END = ">"
ESCAPE = "!"


def solve(stream: str) -> Tuple[int, int]:
    group_score = 0
    garbage_count = 0
    depth = 0
    in_garbage = False
    escape = False
    for c in stream:
        if escape:
            escape = False
        elif in_garbage:
            if c == ESCAPE:
                escape = True
            elif c == GARBAGE_END:
                in_garbage = False
            else:
                garbage_count += 1
        elif c == GARBAGE_START:
            in_garbage = True
        elif c == GROUP_START:
            depth += 1
        elif c == GROUP_END:
            group_score += depth
            depth -= 1
    return group_score, garbage_count


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read()


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
