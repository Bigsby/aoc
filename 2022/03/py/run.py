#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[str]


def get_item_priority(item: str) -> int:
    return (ord(item) - ord('A') + 26 if item < 'a' else ord(item) - ord('a')) + 1


def get_repeated_item_priority(ruckstack: str) -> int:
    cut = len(ruckstack) // 2
    first, second = ruckstack[:cut], ruckstack[cut:]
    for item in first:
        if item in second:
            return get_item_priority(item)
    return 0


def part1(rucksacks: Input) -> int:
    return sum(map(get_repeated_item_priority, rucksacks))


def part2(rucksacks: Input) -> int:
    total = 0
    for index in range(int(len(rucksacks) / 3)):
        first, second, third = rucksacks[index * 3], rucksacks[index * 3 + 1], rucksacks[index * 3 + 2]
        for item in first:
            if item in second and item in third:
                total += get_item_priority(item)
                break
    return total


def solve(puzzle_input: Input) -> Tuple[int, int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


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
