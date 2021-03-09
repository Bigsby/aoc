#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


def has_no_valid_pair(number_index: int, numbers: List[int]) -> bool:
    number = numbers[number_index]
    for test_index in range(number_index - 25, number_index):
        test_number = numbers[test_index]
        for pair_index in range(number_index - 25, number_index):
            if pair_index != test_index and test_number + numbers[pair_index] == number:
                return False
    return True


def get_weakness(numbers: List[int], target_number: int) -> int:
    for start_index in range(0, len(numbers)):
        current_sum = 0
        length = 1
        while current_sum < target_number:
            new_set = numbers[start_index:start_index + length]
            current_sum = sum(new_set)
            if current_sum == target_number:
                return min(new_set) + max(new_set)
            length += 1
    raise Exception("Weakness not found")


def solve(numbers: List[int]) -> Tuple[int, int]:
    part1_result = next(numbers[index] for index in range(
        25, len(numbers)) if has_no_valid_pair(index, numbers))
    return (
        part1_result,
        get_weakness(numbers, part1_result)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(line) for line in file.readlines()]


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
