#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re
from itertools import permutations


def solve(lines: List[List[int]]) -> Tuple[int,int]:
    total1 = 0
    total2 = 0
    for line in lines:
        total1 += max(line) - min(line)
        for number_a, number_b in permutations(line, 2):
            if number_a > number_b and number_a % number_b == 0:
                total2 += number_a // number_b
    return (total1, total2)


line_regex = re.compile(r"\d+")
def get_input(file_path: str) -> List[List[int]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ [ int(i) for i in line_regex.findall(line) ] for line in file.readlines() ]


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