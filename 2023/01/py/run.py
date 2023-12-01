#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict

Input = List[str]


VALUES: Dict[str,int] = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9
}

ALPHA_VALUES: Dict[str,int] = {
    **VALUES,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def get_sum(lines: Input, values: Dict[str,int]) -> int:
    sum = 0
    for line in lines:
        line = line.strip()
        for index in range(len(line)):
            key = next((key for key in values.keys() if line[index:].startswith(key)), "")
            if key:
                sum += values[key] * 10
                break
        for index in range(len(line)):
            key = next((key for key in values.keys() if line[-(index + 1):].startswith(key)), "")
            if key:
                sum += values[key]
                break
    return sum


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (get_sum(puzzle_input, VALUES), get_sum(puzzle_input, ALPHA_VALUES))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return file.readlines()


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
