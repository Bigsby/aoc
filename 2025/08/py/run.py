#! /usr/bin/python3

import sys, os, time
from math import sqrt
from typing import Tuple, List

Point3D = Tuple[int,int,int]
Distances = List[Tuple[float,Point3D,Point3D]]
Input = List[Point3D] 


def calculate_distance(a: Point3D, b: Point3D) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def calculate_pair_distances(junctions: Input) -> Distances:
    distances = []
    for a_index in range(len(junctions)):
        a = junctions[a_index]
        for b_index in range(a_index + 1, len(junctions)):
            b = junctions[b_index]
            distances.append((calculate_distance(a, b), a, b))
    distances.sort()
    return distances


def part1(junctions: Input, distances: Distances) -> int:
    circuits = [ [ junction ] for junction in junctions ]
    for distance, a, b in distances[:1000]:
        contains_a = -1
        contains_b = -1 
        for index, circuit in enumerate(circuits):
            if a in circuit:
                contains_a = index
            if b in circuit:
                contains_b = index
        if contains_a != contains_b:
            circuits[contains_a].extend(circuits[contains_b])
            del circuits[contains_b]
    circuits.sort(key=lambda c: len(c), reverse=True)
    result = 1
    for circuit in circuits[:3]:
        result *= len(circuit)
    return result


def part2(junctions: Input, distances: Distances) -> int:
    circuits = [ [ junction ] for junction in junctions ]
    for distance, a, b in distances:
        contains_a = -1
        contains_b = -1 
        for index, circuit in enumerate(circuits):
            if a in circuit:
                contains_a = index
            if b in circuit:
                contains_b = index
        if contains_a != contains_b:
            circuits[contains_a].extend(circuits[contains_b])
            del circuits[contains_b]
        if len(circuits) == 1:
            return a[0] * b[0]


def solve(puzzle_input: Input) -> Tuple[int,int]:
    distances = calculate_pair_distances(puzzle_input)
    return (part1(puzzle_input, distances), part2(puzzle_input, distances))


def parse_point3d(line: str) -> Point3D:
    split = line.strip().split(',')
    return int(split[0]), int(split[1]), int(split[2])

def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parse_point3d(line) for line in file.readlines() ]


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
