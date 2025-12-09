#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Rotation = Tuple[str,int]
Input = List[Rotation]


def solve(puzzle_input: Input) -> Tuple[int,int]:
    part1 = 0
    part2 = 0

    dial = 50
    started_zero = False
    for (direction, amount) in puzzle_input:
        revolutions, left = divmod(amount, 100)
        part2 += revolutions
        dial += (1 if direction == 'R' else - 1) * left
        if (not started_zero and dial < 0) or dial > 100:
            part2 += 1
        dial %= 100
        started_zero = dial == 0
        if started_zero:
            part1 += 1

    return (part1, part2 + part1)


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [ (line[0], int(line[1:].strip())) for line in file.readlines() ]


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
