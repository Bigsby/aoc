#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Set
from itertools import product
from collections import Counter

Beacon = Tuple[int, int, int]
Scanner = List[Beacon]
Input = List[Scanner]


TEST_SPACE = [(0,1),(1,1),(2,1),(0,-1),(1,-1),(2,-1)]
def try_overlap(known: Scanner, candidate: Scanner) -> Tuple[bool, Scanner, Beacon]:
    new_beacons_differences: List[List[int]] = []
    offset_list: List[int] = []
    for dimension in range(3):
        known_positions = [beacon[dimension] for beacon in known]
        for (test_dimension, test_offset) in TEST_SPACE:
            candidate_positions = [beacon[test_dimension] * test_offset for beacon in candidate]
            differences = [candidate_position - known_position for (known_position , candidate_position) in product(known_positions, candidate_positions)]
            (difference, occurrences) = Counter(differences).most_common(1)[0]
            if occurrences >= 12:
                break
        if occurrences < 12:
            return False, [], (0, 0, 0)
        new_beacons_differences.append([candidate_position - difference for candidate_position in candidate_positions])
        offset_list.append(difference)
    return True, list(zip(new_beacons_differences[0],new_beacons_differences[1],new_beacons_differences[2])), tuple(offset_list)


def solve(scanners: Input) -> Tuple[int, int]:
    known_beacons: Set[Beacon] = set()
    queue: List[Scanner] = [ scanners[0] ]
    scanners_left = scanners[1:]
    offsets: List[Beacon] = [(0,0,0)]
    while queue:
        aligned = queue.pop()
        still_left: List[Scanner] = []
        for candidate in scanners_left:
            success, offset_beacons, offset = try_overlap(aligned, candidate)
            if success:
                offsets.append(offset)
                queue.append(offset_beacons)
            else:
                still_left.append(candidate)
        scanners_left = still_left
        known_beacons.update(aligned)
    return len(known_beacons), max(sum(abs(a-b) for (a,b) in zip(left,right)) for left,right in product(offsets,offsets))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        scanners: Input = []
        scanner: Scanner
        for line in file.readlines():
            line = line.strip()
            if line and line[1] == "-":
                scanner = []
                scanners.append(scanner)
                continue
            if line:
                split = line.split(",")
                scanner.append((int(split[0]), int(split[1]), int(split[2])))
        return scanners


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
