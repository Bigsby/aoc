#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List


def runGenerations(fishes: List[int], generations: int) -> int:
    fishCounts = [ 0 ] * 9
    for fish in fishes:
        fishCounts[fish] += 1
    for _ in range(generations):
        fishesAtZero = fishCounts[0]
        for day in range(8):
            fishCounts[day] = fishCounts[day + 1]
        fishCounts[8] = fishesAtZero
        fishCounts[6] += fishesAtZero
    return sum(fishCounts)


def solve(puzzle_input: str) -> Tuple[int,int]:
    return (runGenerations(puzzle_input, 80), runGenerations(puzzle_input, 256))


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
