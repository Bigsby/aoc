#! /usr/bin/python3

import sys, os, time
from typing import Iterable, List, Tuple
import math


def get_divisors(number: int) -> Iterable[int]:
    large_divisors: List[int] = []
    for i in range(1, int(math.sqrt(number) + 1)):
        if number % i == 0:
            yield i
            if i * i != number:
                large_divisors.append(int(number / i))
    for divisor in reversed(large_divisors):
        yield divisor


def get_present_count_for_house(number: int) -> int:
    return sum(get_divisors(number))


def part1(puzzle_input: int) -> int:
    house_number = 0 
    presents_received = 0
    step = 2 * 3 * 5 * 7 * 11 
    target_presents = puzzle_input / 10
    while presents_received <= target_presents:
        house_number += step
        presents_received = get_present_count_for_house(house_number)
    return house_number


def get_present_count_for_house2(number: int) -> int:
    presents = 0
    for divisor in get_divisors(number):
        if number / divisor < 50:
            presents += divisor * 11
    return presents


def part2(puzzle_input: int, house_number: int) -> int:
    step = 1
    presents_received = 0
    while presents_received <= puzzle_input:
        house_number += step
        presents_received = get_present_count_for_house2(house_number)
    return house_number


def solve(puzzle_input: int) -> Tuple[int,int]:
    part1_result = part1(puzzle_input)
    return (
        part1_result, 
        part2(puzzle_input, part1_result)
    )


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return int(file.read().strip())


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