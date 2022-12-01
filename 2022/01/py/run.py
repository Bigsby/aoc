#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
from functools import reduce

Input = List[List[int]]

def part1(elves: Input) -> int:
    return reduce(lambda current_max, elve: max(current_max, sum(elve)), elves, 0)


def part2(elves: Input) -> int:
    top_elves = [ 0, 0, 0 ]
    for elf in elves:
        elf_sum = sum(elf)
        for index in range(3):
            if elf_sum > top_elves[index]:
                top_elves[index], elf_sum = elf_sum, top_elves[index]
    return sum(top_elves)


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        elves: List[List[int]] = []
        current_elf: List[int] = []
        for line in file.readlines():
            stripped_line = line.strip()
            if stripped_line:
                current_elf.append(int(stripped_line))
            else:
                elves.append(current_elf)
                current_elf = []
        elves.append(current_elf)
        return elves


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
