#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import math

Asteroid = complex


def get_visible_count(asteroid: Asteroid, asteroids: List[Asteroid], maxX: int, maxY: int) -> int:
    asteroids = list(asteroids)
    asteroids.remove(asteroid)
    visible_count = 0
    while asteroids:
        asteroid_to_check = asteroids.pop()
        visible_count += 1
        delta: complex = asteroid_to_check - asteroid
        jump = delta / math.gcd(abs(int(delta.real)), abs(int(delta.imag)))
        asteroid_to_check = asteroid + jump
        while asteroid_to_check.real >= 0 and asteroid_to_check.real <= maxX \
                and asteroid_to_check.imag >= 0 and asteroid_to_check.imag <= maxY:
            if asteroid_to_check in asteroids:
                asteroids.remove(asteroid_to_check)
            asteroid_to_check += jump
    return visible_count


def part1(asteroids: List[Asteroid]) -> Tuple[int, Asteroid]:
    max_x = int(max(map(lambda asteroid: asteroid.real, asteroids)))
    max_y = int(max(map(lambda asteroid: asteroid.imag, asteroids)))
    max_visible_count = 0
    monitoring_station = -1 - 1j
    for asteroid in asteroids:
        visible_count = get_visible_count(asteroid, asteroids, max_x, max_y)
        if visible_count > max_visible_count:
            max_visible_count = visible_count
            monitoring_station = asteroid
    return max_visible_count, monitoring_station


def part2(asteroids: List[Asteroid], monitoring_station: Asteroid) -> int:
    asteroid_angle_distances: Dict[Asteroid, Tuple[float, int]] = {}
    asteroids.remove(monitoring_station)
    for asteroid in asteroids:
        delta = asteroid - monitoring_station
        angle = math.atan2(delta.real, delta.imag) + math.pi
        distance = int(abs(delta.real) + abs(delta.imag))
        asteroid_angle_distances[asteroid] = (angle, distance)
    target_count = 1
    angle = 2 * math.pi
    last_removed = -1 - 1j
    while target_count <= 200:
        asteroid, (angle, _) = min(asteroid_angle_distances.items(),
                                   key=lambda kv: (angle == kv[1][0] or target_count == 1, (angle - kv[1][0]) % (2 * math.pi), kv[1][1]))
        del asteroid_angle_distances[asteroid]
        last_removed = asteroid
        target_count += 1
    return int(last_removed.real) * 100 + int(last_removed.imag)


def solve(asteroids: List[Asteroid]) -> Tuple[int, int]:
    max_visible_count, monitoring_station = part1(asteroids)
    return (
        max_visible_count,
        part2(asteroids, monitoring_station)
    )


def get_input(file_path: str) -> List[Asteroid]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        asteroids: List[Asteroid] = []
        for (y, line) in enumerate(file.readlines()):
            for (x, c) in enumerate(line.strip()):
                if c == "#":
                    asteroids.append(x + y * 1j)
        return asteroids


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
