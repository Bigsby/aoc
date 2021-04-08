#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re
import math
from collections import defaultdict

Values = Tuple[int, ...]
Particle = Tuple[Values, Values, Values]


def get_manhatan_value(values: Values) -> int:
    return abs(values[0]) + abs(values[1]) + abs(values[2])


def part1(particles: List[Particle]) -> int:
    closest_particle = 0
    lowest_acceleration = sys.maxsize
    lowest_position = sys.maxsize
    for index, (position, _, acceleration) in enumerate(particles):
        acceleration_total = get_manhatan_value(acceleration)
        if acceleration_total < lowest_acceleration:
            lowest_acceleration = acceleration_total
            closest_particle = index
            lowest_position = get_manhatan_value(position)
        if acceleration_total == lowest_acceleration and get_manhatan_value(position) < lowest_position:
            closest_particle = index
            lowest_position = get_manhatan_value(position)
    return closest_particle


def get_quadratic_abc(particle_a: Particle, particle_b: Particle, coordinate: int) -> Tuple[float, float, int]:
    p_a_p = particle_a[0][coordinate]
    p_a_a = particle_a[2][coordinate]
    p_a_v = particle_a[1][coordinate] + p_a_a / 2
    p_b_p = particle_b[0][coordinate]
    p_b_a = particle_b[2][coordinate]
    p_b_v = particle_b[1][coordinate] + p_b_a / 2
    return (p_a_a - p_b_a) / 2, p_a_v - p_b_v, p_a_p - p_b_p


def get_colition_times(particle_a: Particle, particle_b: Particle) -> List[int]:
    a, b, c = get_quadratic_abc(particle_a, particle_b, 0)
    times: List[float] = []
    if a == 0:
        if b != 0:
            times.append(-c / b)
    else:
        bb = b * b
        ac4 = a * c * 4
        if bb < ac4:
            return []
        elif bb == ac4:
            times.append(-b / (2 * a))
        else:
            rt = math.sqrt(bb - ac4)
            times.append((-b + rt) / (2 * a))
            times.append((-b - rt) / (2 * a))
    int_times = map(int, filter(lambda t: t >= 0 and round(t) == t, times))
    result: List[int] = []
    for t in int_times:
        collide = True
        for k in [1, 2]:
            a, b, c = get_quadratic_abc(particle_a, particle_b, k)
            if a * t * t + b * t + c != 0:
                collide = False
                break
        if collide:
            result.append(t)
    return result


def part2(particles: List[Particle]) -> int:
    collisions: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for this_index in range(len(particles) - 1):
        for other_index in range(this_index + 1, len(particles)):
            for time in get_colition_times(particles[this_index], particles[other_index]):
                collisions[time].append((this_index, other_index))
    particle_indexes: Set[int] = set(range(len(particles)))
    for time in sorted(list(collisions.keys())):
        collided_to_temove: Set[int] = set()
        for index_a, index_b in collisions[time]:
            if index_a in particle_indexes and index_b in particle_indexes:
                collided_to_temove.add(index_a)
                collided_to_temove.add(index_b)
        particle_indexes -= collided_to_temove
    return len(particle_indexes)


def solve(particles: List[Particle]) -> Tuple[int, int]:
    return (
        part1(particles),
        part2(particles)
    )


line_regex = re.compile(
    r"^p=<(?P<p>[^>]+)>, v=<(?P<v>[^>]+)>, a=<(?P<a>[^>]+)>$")


def parse_line(line: str) -> Particle:
    match = line_regex.match(line)
    if match:
        return \
            tuple(map(int, match.group("p").split(","))), \
            tuple(map(int, match.group("v").split(","))), \
            tuple(map(int, match.group("a").split(",")))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Particle]:
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
