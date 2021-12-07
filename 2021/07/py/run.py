#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Callable

    
def part1(crabs: List[int]) -> int:
    crabs.sort()
    mean = crabs[int(len(crabs) / 2)]
    return sum([ abs(position - mean) for position in crabs ])


def get_distance_cost(pos_a: int, pos_b: int) -> int:
    distance = abs(pos_a - pos_b)
    return int((distance * (distance + 1)) / 2)


def part2(crabs: List[int]) -> int:
    average = int(sum(crabs) / len(crabs))
    return sum([ get_distance_cost(average, position) for position in crabs ])


def solve(puzzle_input: List[int]) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ int(number) for number in file.read().strip().split(',') ]


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
