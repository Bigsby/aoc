#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Set

Motion = Tuple[str, int]
Input = List[Motion]

DIRECTIONS = {
    "R": 1,
    "L": -1,
    "U": -1j,
    "D": 1j
}


def do_motions(motions: Input, tail_count: int) -> int:
    head, tails = 0j, [0j] * tail_count
    visited: Set[complex] = set()
    visited.add(tails[tail_count - 1])
    for direction, length in motions:
        direction_offset = DIRECTIONS[direction]
        for _ in range(length):
            head += direction_offset
            current_head = head
            for index in range(tail_count):
                current_tail = tails[index]
                offset = current_head - current_tail
                if offset == 0:
                    break
                if abs(offset.real) > 1:
                    current_tail = current_tail.real + offset.real / 2 + 1j * \
                        (current_head.imag if abs(offset.imag) <
                         2 else current_tail.imag + offset.imag / 2)
                elif abs(offset.imag) > 1:
                    current_tail = (current_head.real if abs(
                        offset.real) < 2 else current_tail.real + offset.real / 2) + (offset.imag / 2 + current_tail.imag) * 1j
                tails[index] = current_tail
                current_head = current_tail
            visited.add(tails[tail_count - 1])
    return len(visited)


def solve(motions: Input) -> Tuple[int, int]:
    return (do_motions(motions, 1), do_motions(motions, 9))


def process_line(line: str) -> Motion:
    split = line.split()
    return (split[0], int(split[1]))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [process_line(line.strip()) for line in file.readlines()]


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
