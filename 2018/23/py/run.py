#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re

Nanobot = Tuple[int, ...]


def part1(nanobots: List[Nanobot]) -> int:
    max_radius = 0
    strongest_bot: Nanobot = (0, 0, 0, 0)
    for nanobot in nanobots:
        if nanobot[3] > max_radius:
            max_radius = nanobot[3]
            strongest_bot = nanobot
    x0, y0, z0, radius = strongest_bot
    in_range = 0
    for x1, y1, z1, _ in nanobots:
        in_range += abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1) <= radius
    return in_range


def part2(nanobots: List[Nanobot]) -> int:
    all_xs = [bot[0] for bot in nanobots] + [0]
    all_ys = [bot[1] for bot in nanobots] + [0]
    all_zs = [bot[2] for bot in nanobots] + [0]
    xs = (min(all_xs), max(all_xs))
    ys = (min(all_ys), max(all_ys))
    zs = (min(all_zs), max(all_zs))
    location_radius = 1
    while location_radius < xs[1] - xs[0]:
        location_radius *= 2
    while True:
        hightest_count = 0
        best_location: Tuple[int, int, int] = (0, 0, 0)
        shortest_distance = -1
        for x in range(xs[0], xs[1] + 1, location_radius):
            for y in range(ys[0], ys[1] + 1, location_radius):
                for z in range(zs[0], zs[1] + 1, location_radius):
                    count = 0
                    for bot_x, bot_y, bot_z, bot_radius in nanobots:
                        bot_distance = abs(x - bot_x) + \
                            abs(y - bot_y) + abs(z - bot_z)
                        if (bot_distance - bot_radius) // location_radius <= 0:
                            count += 1
                    location_distance = abs(x) + abs(y) + abs(z)
                    if count > hightest_count or \
                            (count == hightest_count and (shortest_distance == -1 or location_distance < shortest_distance)):
                        hightest_count = count
                        shortest_distance = location_distance
                        best_location = (x, y, z)
        if location_radius == 1:
            return shortest_distance
        else:
            xs = (best_location[0] - location_radius,
                  best_location[0] + location_radius)
            ys = (best_location[1] - location_radius,
                  best_location[1] + location_radius)
            zs = (best_location[2] - location_radius,
                  best_location[2] + location_radius)
            location_radius = location_radius // 2


def solve(nanobots: List[Nanobot]) -> Tuple[int, int]:
    return (
        part1(nanobots),
        part2(nanobots)
    )


def parse_line(line: str) -> Nanobot:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_input(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
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
