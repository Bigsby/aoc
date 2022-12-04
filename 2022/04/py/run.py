#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[Tuple[int,int,int,int]]


def has_container(pair: Tuple[int,int,int,int]) -> bool:
    return pair[2] >= pair[0] and pair[3] <= pair[1] \
        or pair[0] >= pair[2] and pair[1] <= pair[3]


def contains_overlap(pair: Tuple[int,int,int,int]) -> bool:
    return pair[2] <= pair[0] <= pair[3] \
        or pair[2] <= pair[1] <= pair[3] \
        or pair[0] <= pair[2] <= pair[1] \
        or pair[0] <= pair[3] <= pair[1]


def solve(pairs: Input) -> Tuple[int,int]:
    return (sum(map(has_container, pairs)), sum(map(contains_overlap, pairs)))


def process_line(line: str) -> Tuple[int,int,int,int]:
    pair = line.strip().split(",")
    first = pair[0].split("-")
    second = pair[1].split("-")
    return int(first[0]), int(first[1]), int(second[0]), int(second[1])


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ process_line(line) for line in file.readlines() ]


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
