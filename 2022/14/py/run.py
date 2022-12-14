#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Set

Input = Set[complex]


def drop_sand(rocks: Input, infite: bool) -> int:
    rocks = set(rocks)
    bottom = int(max(map(lambda rock: rock.imag, rocks))) + (1 if infite else 2)
    if not infite:
        rocks_xs = list(map(lambda rock: int(rock.real), rocks))
        for x in range(min(rocks_xs) - bottom, max(rocks_xs) + bottom):
            rocks.add(x + bottom * 1j)    
    tap = 500 + 0j
    rested_count = 0
    while True:
        unit = tap
        is_rested = False
        while True:
            down = unit + 1j
            down_left = down - 1
            down_right = down + 1
            if down.imag == bottom:
                break
            if (down in rocks) and (down_left in rocks) and (down_right in rocks):
                is_rested = True
                break
            if down not in rocks:
                unit = down
            elif down_left not in rocks:
                unit = down_left
            elif down_right not in rocks:
                unit = down_right
        if infite and (unit.imag == bottom or not is_rested):
            break
        rocks.add(unit)
        rested_count += 1
        if unit == tap:
            break
    return rested_count


def solve(rocks: Input) -> Tuple[int,int]:
    return (drop_sand(rocks, True), drop_sand(rocks, False))


def parse_point(text: str) -> complex:
    split = text.split(',')
    return int(split[0]) + int(split[1]) * 1j


def get_direction(start: complex, end: complex) -> complex:
    if start.real == end.real:
        return 1j if end.imag > start.imag else -1j
    return 1 if end.real > start.real else -1


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        rocks: Set[complex] = set()
        for line in file.readlines():
            points = map(parse_point, line.strip().split(" -> "))
            start = next(points)
            end = next(points)
            while start and end:
                direction = get_direction(start, end)
                while True:
                    rocks.add(start)
                    if start == end:
                        break
                    start += direction
                start = end
                end = next(points, None)
        return rocks


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
