#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def solve(numbers: List[int]) -> Tuple[int, int]:
    TURNS = 30_000_000
    part1_result = 0
    turn = 0
    last_number = numbers[-1]
    occurences = [0] * TURNS
    for number in numbers:
        turn += 1
        occurences[number] = turn
    while turn < TURNS:
        last_occurence = occurences[last_number]
        occurences[last_number] = turn
        if turn == 2020:
            part1_result = last_number
        last_number = turn - last_occurence if last_occurence else 0
        turn += 1
    return part1_result, last_number


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(i) for i in file.read().split(",")]


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
