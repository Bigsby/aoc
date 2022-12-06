#! /usr/bin/python3

import sys, os, time
from typing import Tuple

Input = str

def detect_marker(stream: Input, length: int) -> int:
    for index in range(len(stream) - length):
        if len(set(stream[index:index + length])) == length:
            return index + length
    raise Exception("Marker not found!")


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (detect_marker(puzzle_input, 4), detect_marker(puzzle_input, 14))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
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
