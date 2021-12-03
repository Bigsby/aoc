#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
from collections import Counter

Data = List[int]
Input = (int, Data)

def get_nth_bits_1_count(data: Data, index: int) -> int:
    mask = 1 << index
    return len([1 for number in data if number & mask == mask])

def part1(puzzle_input: Input) -> int:
    bit_length, data = puzzle_input
    gamma = 0
    epsilon = 0
    half = len(data) / 2
    for index in range(bit_length - 1, -1, -1):
        ones_count = get_nth_bits_1_count(data, index)
        gamma = (gamma << 1) + (ones_count > half)
        epsilon = (epsilon << 1) + (ones_count < half)
    return gamma * epsilon

def process_bit(data: Data, index: int, most_common: bool) -> Data:
    if len(data) == 1:
        return data
    ones_count = get_nth_bits_1_count(data, index) 
    zeros_count = len(data) - ones_count
    mask = 1 << index
    match = mask if most_common ^ (ones_count < zeros_count) else 0
    return list(filter(lambda number: number & mask == match, data))


def part2(puzzle_input: Input) -> int:
    bit_length, data = puzzle_input
    oxygen = list(data)
    co2 = list(data)
    index = bit_length - 1
    while len(oxygen) > 1 or len(co2) > 1:
        oxygen = process_bit(oxygen, index, True)
        co2 = process_bit(co2, index, False)
        index -= 1
    return oxygen[0] * co2[0]


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        lines = [ line.strip() for line in file.readlines() ]
        return len(lines[0]), [ int(line, 2) for line in lines ]


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
