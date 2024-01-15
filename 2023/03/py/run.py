#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from collections import defaultdict

Input = List[str]
EngineData = Tuple[Dict[Tuple[int,int],List[int]],List[int]]

def is_symbol(c: str) -> bool:
    return c != "." and not c.isnumeric()


def parse_engine(puzzle_input: Input) -> EngineData:
    gears: Dict[Tuple[int,int],List[int]] = defaultdict(list)
    parts: List[int] = []
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
                symbol = ""
                coord = (0, 0)
                if line_index > 0:
                    for x, c in enumerate(puzzle_input[line_index - 1][search_start:search_end]):
                        if is_symbol(c):
                            is_part = True
                            symbol = c
                            coord = search_start + x, line_index - 1
                            break
                if start_index > 0 and is_symbol(line[search_start]):
                    is_part = True
                    symbol = line[search_start]
                    coord = search_start, line_index
                if start_index + length < line_len and is_symbol(line[search_end - 1]):
                    is_part = True
                    symbol = line[search_end - 1]
                    coord = search_end - 1, line_index
                if not is_part and line_index < len(puzzle_input) - 1:
                    for x, c in enumerate(puzzle_input[line_index + 1][search_start:search_end]):
                        if is_symbol(c):
                            is_part = True
                            symbol = c
                            coord = search_start + x, line_index + 1
                            break
                if is_part:
                    part_number = int(segment)
                    parts.append(part_number)
                    if symbol == "*":
                        gears[coord].append(part_number)
            start_index += length 
    return gears, parts


def part2(engine_data: EngineData) -> int:
    sum = 0
    for parts in engine_data[0].values():
        if len(parts) == 2:
            sum += parts[0] * parts[1]
    return sum


def solve(puzzle_input: Input) -> Tuple[int,int]:
    engine_data = parse_engine(puzzle_input)
    return (sum(engine_data[1]), part2(engine_data))


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
