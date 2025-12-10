#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Range = Tuple[int,int]
Ranges = List[Range]
Input = Tuple[Ranges,List[int]]


def is_in_ranges(ingredient: int, ranges: Ranges) -> bool:
    for start, end in ranges:
        if ingredient >= start and ingredient <= end:
            return True
    return False


def part1(puzzle_input: Input) -> int:
    ranges, ingredients = puzzle_input
    return len([ingredient for ingredient in ingredients if is_in_ranges(ingredient, ranges)])


def aggregate_ranges(ranges: Ranges) -> Ranges:
    ranges.sort()
    changed = True
    while changed:
        changed = False
        for index in range(len(ranges) - 1):
            first_start, first_end = ranges[index]
            second_start, second_end = ranges[index + 1]
            if first_end < second_start or first_start > second_end:
                continue    # don't overlap
            else: 
                ranges[index] = min(first_start, second_start), max(first_end, second_end)
                del ranges[index + 1]
                changed = True
                break
    return ranges


def part2(puzzle_input: Input) -> int:
    ranges, _ = puzzle_input
    aggregated_ranges = aggregate_ranges(ranges)
    ingredients = 0
    for start, end in aggregated_ranges:
        ingredients += end - start + 1
    return ingredients


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        ranges: Ranges = []
        ingredients: List[int] = []
        in_ranges = True
        for line in file.readlines():
            stripped = line.strip()
            if in_ranges:
                if not stripped:
                    in_ranges = False
                    continue
                split = stripped.split('-')
                ranges.append((int(split[0]), int(split[1])))
            else:
                ingredients.append(int(stripped))
        return ranges, ingredients


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
