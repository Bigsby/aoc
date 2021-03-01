#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import combinations
from functools import reduce


def get_combination(numbers: List[int], length: int) -> int:
    for combination in combinations(numbers, length):
        if sum(combination) == 2020:
            return reduce(lambda acc, number: acc * number, combination)
    raise Exception("Numbers not found")


def solve(numbers: List[int]) -> Tuple[int,int]:
    return (
        get_combination(numbers, 2),
        get_combination(numbers, 3)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ int(line) for line in file.readlines() ]


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