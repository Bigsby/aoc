#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def get_count(numbers: List[int], index_offset: int) -> int:
    count = 0
    for index in range(len(numbers)):
        if numbers[index] == numbers[(index + index_offset) % len(numbers)]:
            count += numbers[index]
    return count


def solve(numbers: List[int]) -> Tuple[int,int]:
    return (
        get_count(numbers, len(numbers) - 1),
        get_count(numbers, len(numbers) // 2)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ int(c) for c in file.read().strip() ]


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