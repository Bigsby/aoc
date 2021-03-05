#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def solve(numbers: List[int]) -> Tuple[int, int]:
    numbers_length = len(numbers)
    previous_lists: List[List[int]] = []
    cycles = 0
    current_list = list(numbers)
    while True:
        if current_list in previous_lists:
            return cycles, previous_lists.index(current_list)
        cycles += 1
        previous_lists.append(list(current_list))
        update_index = -1
        max_number = 0
        for index, number in enumerate(current_list):
            if number > max_number:
                max_number = number
                update_index = index
        current_list[update_index] = 0
        while max_number:
            update_index = update_index + 1 if update_index < numbers_length - 1 else 0
            current_list[update_index] += 1
            max_number -= 1


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(i) for i in file.read().split("\t")]


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
