#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from functools import reduce

MARKS_COUNT = 256


def run_lengths(marks: List[int], lengths: List[int], current_mark: int, skip: int) -> Tuple[List[int], int, int]:
    for length in lengths:
        to_reverse: List[int] = []
        reverse_mark = current_mark
        for _ in range(length):
            to_reverse.append(marks[reverse_mark])
            reverse_mark = (reverse_mark + 1) % MARKS_COUNT
        reverse_mark = current_mark
        for _ in range(length):
            marks[reverse_mark] = to_reverse.pop()
            reverse_mark = (reverse_mark + 1) % MARKS_COUNT
        current_mark = (current_mark + length + skip) % MARKS_COUNT
        skip += 1
    return marks, current_mark, skip


def part1(puzzle_input: str):
    lengths = [int(c) for c in puzzle_input.split(",")]
    marks = [i for i in range(MARKS_COUNT)]
    marks, *_ = run_lengths(marks, lengths, 0, 0)
    return marks[0] * marks[1]


SUFFIX = [17, 31, 73, 47, 23]


def part2(puzzle_input: str):
    lengths = [ord(c) for c in puzzle_input]
    lengths.extend(SUFFIX)
    marks = [i for i in range(MARKS_COUNT)]
    current_mark = skip = 0
    for _ in range(64):
        marks, current_mark, skip = run_lengths(
            marks, lengths, current_mark, skip)
    dense_hash = map(lambda index:
                     reduce(lambda soFar, mark:
                            soFar ^ mark, marks[index * 16:(index + 1) * 16]), range(16))
    return "".join(map(lambda knot: f"{knot:02x}", dense_hash))


def solve(puzzle_input: str) -> Tuple[int, str]:
    return (
        part1(puzzle_input),
        part2(puzzle_input)
    )


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


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
