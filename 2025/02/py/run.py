#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[Tuple[int,int]]


def is_invalid1(id: int) -> bool:
    string_value = str(id)
    length = len(string_value)
    if length % 2 == 1:
        return False
    half = length // 2
    return string_value[:half] == string_value[half:]


def part1(puzzle_input: Input) -> int:
    invalid_sum = 0
    for start, end in puzzle_input:
        for id in range(start, end + 1):
            if is_invalid1(id):
                invalid_sum += id
    return invalid_sum


def get_divisors(n):
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            yield i, n // i


def is_invalid2(id: int) -> bool:
    string_value = str(id)
    length = len(string_value)
    for divisor, count in get_divisors(length):
        if string_value == (string_value[:divisor] * count):
            return True
    return False


def part2(puzzle_input: Input) -> int:
    invalid_sum = 0
    for start, end in puzzle_input:
        for id in range(start, end + 1):
            if is_invalid2(id):
                invalid_sum += id
    return invalid_sum


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def parse_range(part: str) -> Tuple[int,int]:
    split = part.split('-')
    return int(split[0]), int(split[1])


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [parse_range(part) for part in file.read().strip().split(',')]


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
