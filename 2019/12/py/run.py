#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re
import math
from copy import deepcopy
from itertools import combinations
from functools import reduce

Coordinates = Tuple[int, int, int]


class Moon():
    def __init__(self, x: int, y: int, z: int):
        self.position: Coordinates = (x, y, z)
        self.velocity: Coordinates = (0, 0, 0)

    @staticmethod
    def get_delta(this_value: int, other_value: int) -> int:
        if this_value < other_value:
            return 1
        if this_value > other_value:
            return -1
        return 0

    def get_moon_elta(self, other_moon: Coordinates) -> Coordinates:
        return (
            Moon.get_delta(self.position[0], other_moon[0]),
            Moon.get_delta(self.position[1], other_moon[1]),
            Moon.get_delta(self.position[2], other_moon[2])
        )

    @staticmethod
    def sum(one: Coordinates, two: Coordinates) -> Coordinates:
        return (one[0] + two[0], one[1] + two[1], one[2] + two[2])
    
    @staticmethod
    def sum_abs(coordinate: Coordinates) -> int:
        return abs(coordinate[0]) + abs(coordinate[1]) + abs(coordinate[2])

    def update_velocity(self, other_moon: Coordinates):
        self.velocity = Moon.sum(self.velocity, self.get_moon_elta(other_moon))

    def update_position(self):
        self.position = Moon.sum(self.position, self.velocity)

    def get_total_energy(self) -> int:
        return Moon.sum_abs(self.position) * Moon.sum_abs(self.velocity)

    def __str__(self):
        return f"{self.position} {self.velocity}"

    def __repr__(self) -> str:
        return self.__str__()


def run_step(moons: List[Moon]):
    for moon_a, moon_b in combinations(moons, 2):
        moon_a.update_velocity(moon_b.position)
        moon_b.update_velocity(moon_a.position)
    for moon in moons:
        moon.update_position()


def part1(moons: List[Moon]) -> int:
    step = 1000
    moons = deepcopy(moons)
    while step:
        step -= 1
        run_step(moons)
    return sum(map(lambda moon: moon.get_total_energy(), moons))


def build_state_for_coordinate(coordinate: int, moons: List[Moon]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    return (tuple(moon.position[coordinate] for moon in moons), tuple(moon.velocity[coordinate] for moon in moons))


def part2(moons: List[Moon]) -> int:
    step = 0
    initial_states = [build_state_for_coordinate(
        coordinate, moons) for coordinate in range(3)]
    cyles = [0] * 3
    while not all(cyles):
        step += 1
        run_step(moons)
        for coordinate in range(3):
            if not cyles[coordinate]:
                current_state = build_state_for_coordinate(coordinate, moons)
                if current_state == initial_states[coordinate]:
                    cyles[coordinate] = step
    return reduce(lambda soFar, cycle: soFar * cycle // math.gcd(soFar, cycle), cyles)


def solve(moons: List[Moon]) -> Tuple[int, int]:
    return (
        part1(moons),
        part2(moons)
    )


line_regex = re.compile(
    r"^<x=(?P<x>-?\d+),\sy=(?P<y>-?\d+),\sz=(?P<z>-?\d+)>$")


def parse_line(line: str) -> Moon:
    match = line_regex.match(line)
    if match:
        return Moon(int(match.group("x")), int(match.group("y")), int(match.group("z")))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Moon]:
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
