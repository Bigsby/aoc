#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Iterable

Input = List[List[int]]


def get_neighbors(x: int, y: int) -> Iterable[Tuple[int,int]]:
    if x:
        yield (x - 1, y)
        if y:
            yield (x - 1, y - 1)
        if y < 9:
            yield (x - 1, y + 1)
    if x < 9:
        yield (x + 1, y)
        if y:
            yield (x + 1, y - 1)
        if y < 9:
            yield (x + 1, y + 1)
    if y:
        yield (x, y - 1)
    if y < 9:
        yield (x, y + 1)


def solve(octopuses: Input) -> Tuple[int, int]:
    flashes = 0
    all_flashes = 0
    step = 0
    while not all_flashes or step < 100:
        step += 1
        step_flashes = 0
        to_process = []
        for y in range(10):
            for x in range(10):
                octopuses[y][x] += 1
                if octopuses[y][x] > 9:
                    to_process.append((x, y))
        while (len(to_process)):
            x, y = to_process.pop()
            if octopuses[y][x] == 0:
                continue
            step_flashes += 1
            octopuses[y][x] = 0
            for neighbor_x, neighbor_y in get_neighbors(x, y):
                if octopuses[neighbor_y][neighbor_x] == 0:
                    continue
                octopuses[neighbor_y][neighbor_x] += 1
                if octopuses[neighbor_y][neighbor_x] > 9:
                    to_process.append((neighbor_x, neighbor_y))
        if step < 100:
            flashes += step_flashes
        if step_flashes == 100:
            all_flashes = step
    return flashes, all_flashes


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ [ int(c) for c in line.strip() ] for line in file.readlines() ]


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
