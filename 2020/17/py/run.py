#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple

Coordinate = Tuple[int, ...]
Universe = Dict[Coordinate, bool]


def get_limits(universe: Universe) -> Tuple[Coordinate, Coordinate]:
    lower_limit: List[int] = []
    upper_limit: List[int] = []
    for index in range(len(list(universe.keys())[0])):
        lower_limit.append(min(key[index] for key in universe.keys()))
        upper_limit.append(max(key[index] for key in universe.keys()))
    return (tuple(lower_limit), tuple(upper_limit))


OUTER_DIMENSIONS = ["z", "w"]


def print_universe(universe: Universe):
    lower_limit, upper_limit = get_limits(universe)
    dimension_count = len(list(universe.keys())[0])
    for coordinate in cycle_coordinates(lower_limit, upper_limit):
        if coordinate[-1] == lower_limit[-1] and coordinate[-2] == lower_limit[-2]:
            print("\n" + ", ".join(OUTER_DIMENSIONS[index] + "=" + str(
                coordinate[index]) for index in range(dimension_count - 2)), end="")
        if coordinate[-1] == lower_limit[-1]:
            print()
        print('#' if universe[coordinate] else '.', end="")
    print()
    input()


def previous(coordinate: Coordinate) -> Coordinate:
    value_list = list(coordinate)
    value_list[-1] -= 1
    return tuple(value_list)


def under(coordinate: Coordinate) -> Coordinate:
    return tuple(v - 1 for v in coordinate)


def over(coordinate: Coordinate) -> Coordinate:
    return tuple(v + 1 for v in coordinate)


def add_dimension(coordiate: Coordinate) -> Coordinate:
    return tuple([0] + list(coordiate))


def next_coordinateValue(current: Coordinate, lower_limit: Coordinate, upper_limit: Coordinate) -> Coordinate:
    result = list(current)
    for index in range(len(current) - 1, -1, -1):
        if current[index] < upper_limit[index]:
            result[index] += 1
            for overflow in range(index + 1, len(current)):
                result[overflow] = lower_limit[overflow]
            break
    return tuple(result)


def cycle_coordinates(lower_limit: Coordinate, upper_limit: Coordinate) -> Iterable[Coordinate]:
    current = previous(lower_limit)
    while (current != upper_limit):
        current = next_coordinateValue(current, lower_limit, upper_limit)
        yield current


def get_neighbor_active_count(universe: Universe, coordinate: Coordinate) -> int:
    return sum(neighbor != coordinate and neighbor in universe and universe[neighbor]
               for neighbor in cycle_coordinates(under(coordinate), over(coordinate)))


def next_cycle(universe: Universe) -> Universe:
    new_state: Universe = dict()
    lower_limit, upper_limit = get_limits(universe)
    for coordinate in cycle_coordinates(under(lower_limit), over(upper_limit)):
        active_neighbor_count = get_neighbor_active_count(universe, coordinate)
        # print(coordinate, active_neighbor_count)
        new_value = False
        if coordinate in universe and universe[coordinate]:
            new_value = active_neighbor_count == 2 or active_neighbor_count == 3
        else:
            new_value = active_neighbor_count == 3
        new_state[coordinate] = new_value
    # input()
    return new_state


def run_cycles(universe: Universe) -> int:
    # print_universe(universe)
    for _ in range(6):
        universe = next_cycle(universe)
        # print_universe(universe)
    return sum(universe.values())


def solve(universe: Universe) -> Tuple[int, int]:
    return (
        run_cycles(universe),
        run_cycles({add_dimension(coordinate): value for coordinate,
                    value in universe.items()})
    )


def get_input(file_path: str) -> Universe:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    universe: Universe = dict()
    with open(file_path, "r") as file:
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                universe[(0, y, x)] = c == "#"
    return universe


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
