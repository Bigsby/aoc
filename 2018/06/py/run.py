#! /usr/bin/python3

import sys, os, time
from typing import List, Dict, Set, Tuple
from itertools import product


def get_manhatan_distance(location_a: complex, location_b: complex) -> int:
    return int(abs(location_a.real - location_b.real) + abs(location_a.imag - location_b.imag))


def get_map_edges(locations: List[complex]) -> Tuple[int, int, int, int]:
    return  int(min(map(lambda i: i.real, locations))) - 1, \
            int(max(map(lambda i: i.real, locations))) + 1, \
            int(min(map(lambda i: i.imag, locations))) - 1, \
            int(max(map(lambda i: i.imag, locations))) + 1


def find_closest_location(map_location: complex, locations: List[complex]) -> int:
    closest = -1
    closest_distance = sys.maxsize
    for index, location in enumerate(locations):
        distance = get_manhatan_distance(map_location, location)
        if distance < closest_distance:
            closest = index
            closest_distance = distance
        elif distance == closest_distance:
            closest = -1
    return closest


def part1(locations: List[complex]) -> int:
    start_x, end_x, start_y, end_y = get_map_edges(locations)
    map_locations: Dict[complex,int] = {}
    location_counts: List[int] = [ 0 ] * len(locations)

    for map_location_x, map_location_y in product(range(start_x, end_x + 1), range(start_y, end_y + 1)):
        map_location = map_location_x + map_location_y * 1j
        closest = find_closest_location(map_location, locations)
        map_locations[map_location] = closest
        if closest != -1:
            location_counts[closest] += 1
    
    edge_locations: Set[int] = set()
    for y in range(start_y, end_y + 1):
        edge_locations.add(map_locations[start_x + y * 1j])
        edge_locations.add(map_locations[end_x + y * 1j])
    for x in range(start_x, end_x + 1):
        edge_locations.add(map_locations[x + start_y * 1j])
        edge_locations.add(map_locations[x + end_y * 1j])
    return max([ value for index, value in enumerate(location_counts) if index not in edge_locations ])


MAX_DISTANCE = 10000
def part2(locations: List[complex]) -> int:
    start_x, end_x, start_y, end_y = get_map_edges(locations)
    valid_locations_count = 0
    for map_location_x, map_location_y in product(range(start_x, end_x + 1), range(start_y, end_y + 1)):
        map_location = map_location_x + map_location_y * 1j
        total_distances = sum(map(lambda location: get_manhatan_distance(location, map_location), locations))
        if total_distances < MAX_DISTANCE:
            valid_locations_count += 1
    return valid_locations_count


def solve(locations: List[complex]) -> Tuple[int,int]:
    return (
        part1(locations),
        part2(locations)
    )


def parse_line(line: str) -> complex:
    split_line: List[str] = line.split(",")
    return int(split_line[0].strip()) + int(split_line[1].strip()) * 1j


def get_input(file_path: str) -> List[complex]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ parse_line(line) for line in file.readlines() ]


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