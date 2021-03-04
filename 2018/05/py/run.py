#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


def part1(polymer: str) -> int:
    polymer_ints = [ ord(c) for c in polymer]
    had_changes = True
    while had_changes:
        had_changes = False
        index = 0
        while index < len(polymer_ints) - 1:
            if abs(polymer_ints[index] - polymer_ints[index + 1]) == 32:
                del polymer_ints[index]
                del polymer_ints[index]
                had_changes = True
            else:      
                index += 1
    return len(polymer_ints)


def part2(polymer: str) -> int:
    min_units = sys.maxsize
    for c_ord in range(ord("A"), ord("Z") + 1):
        stripped_polymer = polymer.replace(chr(c_ord), "")
        stripped_polymer = stripped_polymer.replace(chr(c_ord + 32), "")
        min_units = min(min_units, part1(stripped_polymer))
    return min_units


def solve(polymer: str) -> Tuple[int,int]:
    return (
        part1(polymer),
        part2(polymer)
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