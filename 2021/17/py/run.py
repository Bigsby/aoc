#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Iterable
import re
import math

Input = Tuple[int, int, int, int]


def is_direction_valid(target_area: Input, direction: Tuple[int,int]) -> bool:
    (x1, x2, y1, y2) = target_area
    current_x = 0
    current_y = 0
    direction_x, direction_y = direction
    while current_x <= x2 and current_y >= y1:
        current_x += direction_x
        current_y += direction_y
        if current_x >= x1 and current_x <= x2 and current_y >= y1 and current_y <= y2:
            return True
        direction_x = 0 if direction_x == 0 else direction_x - 1
        direction_y -= 1
    return False


def count_valid_in_range(target_area: Input, x_range: Iterable[int], y_range: Iterable[int]) -> int:
    count = 0
    for x in x_range:
        for y in y_range:
            count += is_direction_valid(target_area, (x, y))
    return count


def solve(target_area: Input) -> Tuple[int,int]:
    (x1, x2, y1, y2) = target_area
    part2 = (x2 - x1 + 1) * (-y1 + y2 + 1)
    part2 += count_valid_in_range(
        target_area,
        range(math.ceil((math.sqrt(8 * x1 + 1) -1) // 2), x2 // 2 + 2),
        range(y2 + 1, -y1)
    )
    y_direction = -y1 - 1
    return ((y_direction * (y_direction + 1)) // 2, part2)


input_regex = re.compile(r"target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)")
def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        input_match = input_regex.match(file.read().strip())
        if input_match:
            return (
                int(input_match.group("x1")),
                int(input_match.group("x2")),
                int(input_match.group("y1")),
                int(input_match.group("y2"))
            )
        raise Exception("Bad input format")


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
