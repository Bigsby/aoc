#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Set, Generator, List

Input = Set[complex]

def get_maxs(rolls: Set[complex]) -> Tuple[int, int]:
    return int(max(p.real for p in rolls)), int(max(p.imag for p in rolls))

ADJACENT: List[complex] = [
        -1 -1j, -1j, 1 -1j,
        -1    ,      1,
        -1 +1j,  1j, 1 +1j
        ]
def get_adjacent(current: complex, max_x: int, max_y: int) -> Generator[complex, None, None]:
    for adjacent in ADJACENT:
        neighbor = current + adjacent
        if neighbor.real >= 0 and neighbor.real <= max_x and \
                neighbor.imag >= 0 and neighbor.imag <= max_y:
            yield neighbor


def get_accessible_rolls(puzzle_input: Input, max_x: int, max_y: int) -> List[complex]:
    accessible_rolls: List[complex] = []
    for roll in puzzle_input:
        adjacent_rolls = [ p for p in get_adjacent(roll, max_x, max_y) if p in puzzle_input]
        if len(adjacent_rolls) < 4:
            accessible_rolls.append(roll)
    return accessible_rolls


def part1(puzzle_input: Input) -> int:
    max_x, max_y = get_maxs(puzzle_input)
    accessible_rolls = get_accessible_rolls(puzzle_input, max_x, max_y)
    return len(accessible_rolls)


def part2(puzzle_input: Input) -> int:
    max_x, max_y = get_maxs(puzzle_input)
    removed = 0
    while True:
        accessible_rolls = get_accessible_rolls(puzzle_input, max_x, max_y)
        if len(accessible_rolls) != 0:
            removed += len(accessible_rolls)
            puzzle_input = puzzle_input - set(accessible_rolls)
        else:
            break
    return removed


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        rolls = set()
        for row, line in enumerate(file.readlines()):
            for column, c in enumerate(line.strip()):
                if c == '@':
                    rolls.add(row + column * 1j)
        return rolls


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
