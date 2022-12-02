#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple, List
from functools import reduce

Input = List[Tuple[int, int]]


def hand_result(elf: int, me: int) -> int:
    if elf == me:
        return 1
    return 2 * ((elf + 1) % 3 == me)


def part1(puzzle_input: Input) -> int:
    return reduce(lambda score, hand: score + 3 * hand_result(hand[0], hand[1]) + hand[1] + 1, puzzle_input, 0)


def part2(puzzle_input: Input) -> int:
    return reduce(lambda score, hand: score + 1 + hand[1] * 3 + (hand[0] + hand[1] - 1) % 3, puzzle_input, 0)


def solve(puzzle_input: Input) -> Tuple[int, int]:
    return (part1(puzzle_input), part2(puzzle_input))


def process_line(line: str) -> Tuple[int, int]:
    return (ord(line[0]) - ord('A'), ord(line[2]) - ord('X'))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [process_line(line) for line in file.readlines()]


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

# A 0 Rock
# B 1 Paper
# C 2 Scissors
#
# X 0 Rock
# Y 1 Paper
# Z 2 Scissors
