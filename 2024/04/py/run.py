#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Optional

Input = List[str]

DIRECTIONS: List[Tuple[int,int]] = [      \
            (-1, -1), ( 0, -1), ( 1, -1), \
            (-1,  0),           ( 1,  0), \
            (-1,  1), ( 0,  1), ( 1,  1)  \
        ]

def try_get_neighbour(puzzle_input: Input, x: int, y: int, go_x: int, go_y: int, letter: str) -> Optional[Tuple[int,int]]:
    new_x = x + go_x
    new_y = y + go_y
    if new_x >= 0 \
        and new_x < len(puzzle_input[0]) \
        and new_y >= 0 \
        and new_y < len(puzzle_input) \
        and puzzle_input[new_y][new_x] == letter:
        return (new_x, new_y)
    return None


LETTERS = [ "M", "A", "S" ]

def has_XMAS(puzzle_input: Input, x: int, y: int, go_x: int, go_y: int) -> bool:
    for letter in LETTERS:
        neighbour = try_get_neighbour(puzzle_input, x, y, go_x, go_y, letter)
        if not neighbour:
            return False
        x, y = neighbour
    return True


def part1(puzzle_input: Input) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)
    total = 0
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] != "X":
                continue
            for (go_x, go_y) in DIRECTIONS:
                if has_XMAS(puzzle_input, x, y, go_x, go_y):
                    total += 1
    return total 


def has_MAS(puzzle_input: Input, x: int, y: int, go_x: int, go_y: int) -> bool:
    return try_get_neighbour(puzzle_input, x, y, go_x, go_y, "M") \
            and try_get_neighbour(puzzle_input, x, y, -go_x, -go_y, "S") \
            or try_get_neighbour(puzzle_input, x, y, go_x, go_y, "S") \
            and try_get_neighbour(puzzle_input, x, y, -go_x, -go_y, "M")


def has_X_MAS(puzzle_input: Input, x: int, y: int) -> bool:
    return has_MAS(puzzle_input, x, y, 1, 1) and has_MAS(puzzle_input, x, y, -1, 1)


def part2(puzzle_input: Input) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)
    total = 0
    for y in range(height):
        for x in range(width):
            if puzzle_input[y][x] == "A" and has_X_MAS(puzzle_input, x, y):
                total += 1
    return total 


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


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
