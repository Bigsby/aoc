#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

TriangleSides = List[List[int]]


def is_possible_triangle(side_a: int, side_b: int, side_c: int) -> bool:
    return side_a < (side_b + side_c) \
            and side_b < (side_a + side_c) \
            and side_c < (side_a + side_b)


def solve(triangle_sides: TriangleSides) -> Tuple[int,int]:
    return (
        sum(is_possible_triangle(sideA, sideB, sideC) for sideA, sideB, sideC in triangle_sides), 
        sum(map(lambda index: is_possible_triangle(\
                triangle_sides[(index // 3) * 3][index % 3], \
                triangle_sides[(index // 3) * 3 + 1][index % 3], \
                triangle_sides[(index // 3) * 3 + 2][index % 3]), \
                range(len(triangle_sides))
        ))
    )


line_regex = re.compile(r"\d+")
def parse_line(line: str) -> List[int]:
    return [ int(i) for i in  line_regex.findall(line) ]


def get_input(file_path: str) -> List[List[int]]:
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