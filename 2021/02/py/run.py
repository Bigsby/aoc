#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Command = Tuple[complex, int]


def part1(commands: List[Command]) -> int:
    position = 0j
    for command in commands:
        position += command[1] * command[0]
    return int(position.real * position.imag)


def part2(commands: List[Command]) -> int:
    position = 0j
    aim = 0j
    for command in commands:
        if command[0] == 1:
            position += command[1] * (1 + aim)
        else:
            aim += command[1] * command[0]
    return int(position.real * position.imag)


def solve(commands: List[Command]) -> Tuple[int, int]:
    return (part1(commands), part2(commands))


def parse_line(line: str) -> Command:
    split = line.split(" ")
    units = int(split[1])
    if split[0] == "forward":
        return 1 + 0j, units
    if split[0] == "down":
        return 0 + 1j, units
    if split[0] == "up":
        return 0 - 1j, units
    raise Exception(f"Unknown direction {split[0]}")


def get_input(file_path: str) -> List[Command]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [parse_line(line) for line in file.readlines()]


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
