#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = Tuple[List[int],List[int]]

def part1(puzzle_input: Input) -> int:
    left, right = puzzle_input
    left = list(left)
    right = list(right)
    left.sort()
    right.sort()
    distance_total = 0
    while left:
        distance_total += abs(right.pop(0) - left.pop(0))
    return distance_total


def part2(puzzle_input: Input) -> int:
    left, right = puzzle_input
    similarity_score = 0
    for id in left:
        similarity_score += id * right.count(id)
    return similarity_score


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        left = []
        right = []
        for line in file.readlines():
            split = list(filter(None, line.split()))
            left.append(int(split[0]))
            right.append(int(split[1]))
        return (left, right)


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
