#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[str]

def is_symbol(c: str) -> bool:
    return not c.isnumeric() and c != "."


def part1(puzzle_input: Input) -> int:
    sum = 0
    for line_index in range(len(puzzle_input)):
        line = puzzle_input[line_index].strip()
        line_len = len(line)
        start_index = 0
        while start_index < line_len and not line[start_index].isnumeric():
            start_index += 1
        while start_index < line_len:
            length = 1
            while start_index + length <= line_len and line[start_index:start_index + length].isnumeric():
                length += 1
            segment = line[start_index:start_index + length - 1]
            if segment.isnumeric():
                search_start = max(0, start_index - 1)
                search_end = min(line_len, start_index + length)
                is_part = False
                if line_index > 0:
                    for c in puzzle_input[line_index - 1][search_start:search_end]:
                        if is_symbol(c):
                            is_part = True
                            break;
                is_part |= (start_index > 0 and is_symbol(line[search_start])) | (start_index + length < line_len and is_symbol(line[search_end - 1]))
                if not is_part and line_index < len(puzzle_input) - 1:
                    for c in puzzle_input[line_index + 1][search_start:search_end]:
                        if is_symbol(c):
                            is_part = True
                            break;
                if is_part:
                    sum += int(segment)
            start_index += length 
    return sum


def find_adjacent_parts(puzzle_input: Input, line: int, gear: int) -> List[int]:
    print(puzzle_input[line][gear], line, gear)
    return []


def part2(puzzle_input: Input) -> int:
    sum = 0
    for line_index, line in enumerate(puzzle_input):
        for gear_index, c in enumerate(line.strip()):
            if c == "*":
                find_adjacent_parts(puzzle_input, line_index, gear_index)


    return sum


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return file.readlines()


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
