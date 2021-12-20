#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict

Beacon = Tuple[int, int, int]
Scanner = Tuple[int,List[Beacon]]
Input = List[Scanner]


def build_relative_positions(beacons: List[Beacon]) -> Dict[Beacon, List[Beacon]]:
    result: Dict[Beacon, List[Beacon]] = {}
    for this in range(len(beacons)):
        this_beacon = beacons[this]
        result[this_beacon] = []
        for that in range(len(beacons)):
            if this != that:
                result[this_beacon].append((
                    abs(this_beacon[0] - beacons[that][0]),
                    abs(this_beacon[1] - beacons[that][1]),
                    abs(this_beacon[2] - beacons[that][2])
                ))
    return result


def are_rotation_equal(a: Beacon, b: Beacon) -> bool:
    return a[0] in b and a[1] in b and a[2] in b


def relative_match(relative: Beacon, offsets: List[Beacon]) -> bool:
    for offset in offsets:
        if relative[0] in offset and relative[1] in offset and relative[2] in offset:
            return True
    return False


def find_overlapping_beacons(known_beacons: Dict[Beacon,List[Beacon]], current: Dict[Beacon,List[Beacon]]) -> List[Tuple[Beacon, Beacon]]:
    result: List[Tuple[Beacon, Beacon]] = []
    for beacon, relatives in current.items():
        for distinct, distinct_relatives in known_beacons.items():
            if len(list(filter(lambda relative: relative_match(relative, distinct_relatives), relatives))) > 1:
                result.append((distinct, beacon))
                #if len(result) > 11:
                    #return result
    return result


def populate_relatives_positions(known_beacons: Dict[Beacon, List[Beacon]]):
    for this in known_beacons.keys():
        for that in known_beacons.keys():
            if this == that:
                continue
            offset = (
                abs(this[0] - that[0]),
                abs(this[1] - that[1]),
                abs(this[2] - that[2])
            )
            if offset not in known_beacons[this]:
                known_beacons[this].append(offset)


def find_difference(first_left: Beacon, first_right: Beacon, second_left: Beacon, second_right: Beacon, left_index: int, right_index: int) -> Tuple[int, int]:
    f1 = first_left[left_index] + first_right[right_index]
    f2 = second_left[left_index] + second_right[right_index]
    difference = f1 if f1 == f2 else first_left[left_index] - first_right[right_index]
    flip = 1 if first_left[left_index] - difference == first_right[right_index] else -1
    return (difference, flip)


def get_offset(overlapping: List[Tuple[Beacon, Beacon]], rotation: Beacon) -> Tuple[Beacon, Beacon, Beacon]:
    first_left, first_right = overlapping[0]
    second_left, second_right = overlapping[1]
    difference_flip = (
        find_difference(first_left, first_right, second_left, second_right, 0, rotation[0]),
        find_difference(first_left, first_right, second_left, second_right, 1, rotation[1]),
        find_difference(first_left, first_right, second_left, second_right, 2, rotation[2])
    )
    return (
        (
            difference_flip[0][0],
            difference_flip[1][0],
            difference_flip[2][0]
        ),
        (
            difference_flip[0][1],
            difference_flip[1][1],
            difference_flip[2][1]
        ),
        rotation
    )

def add_beacon(beacon: Beacon, offset: Tuple[Beacon, Beacon, Beacon]) -> Beacon:
    ((diff_x, diff_y, diff_z),(flip_x, flip_y, flip_z), (rotation_x, rotation_y, rotation_z)) = offset
    return (
        (beacon[rotation_x] + diff_x * flip_x) * flip_x,
        (beacon[rotation_y] + diff_y * flip_y) * flip_y,
        (beacon[rotation_z] + diff_z * flip_z) * flip_z
    )


def get_rotation(overlapping_pairs, known_beacons, current_beacon) -> Beacon:
    known, found = overlapping_pairs[0]
    for found_relative in current_beacon[found]:
        for known_relative in known_beacons[known]:
            if are_rotation_equal(found_relative, known_relative):
                return (
                    found_relative.index(known_relative[0]),
                    found_relative.index(known_relative[1]),
                    found_relative.index(known_relative[2]),
                )
    raise Exception("Rotation not found")


def get_manhatandistance(position_a: Beacon, position_b: Beacon) -> int:
    return abs(position_a[0] - position_b[0]) + abs(position_a[1] - position_b[1]) + abs(position_a[2] - position_b[2])


def solve(scanners: Input) -> int:
    scanner_positions: List[Tuple[Beacon, Beacon]] = [((0,0,0),(0,0,0),(0,1,2))] * len(scanners)
    known_beacons: Dict[Beacon,List[Beacon]] = {}
    scanner_relative_positions: List[Dict[Beacon, List[Beacon]]] = []
    for _, beacons in scanners:
        scanner_relative_positions.append(build_relative_positions(beacons))
    for beacon in scanners[0][1]:
        known_beacons[beacon] = []
    populate_relatives_positions(known_beacons)
    scanners_left = scanners[1:]
    while len(scanners_left):
        not_matched: List[Scanner] = []
        for scanner in scanners_left:
            id, beacons = scanner
            this_relative = scanner_relative_positions[id]
            overlapping_pairs = find_overlapping_beacons(known_beacons, this_relative)
            if len(overlapping_pairs) > 11:
                rotation = get_rotation(overlapping_pairs, known_beacons, this_relative)
                offset = get_offset(overlapping_pairs, rotation)
                scanner_positions[id] = offset
                overlapping: List[beacon] = list(map(lambda pair: pair[1], overlapping_pairs))
                for beacon in beacons:
                    if beacon not in overlapping:
                        known_beacons[add_beacon(beacon, offset)] = []
                populate_relatives_positions(known_beacons)
            else:
                not_matched.append(scanner)
        scanners_left = not_matched
    maximum = 0
    for this in range(len(scanners)):
        for that in range(len(scanners)):
            if this != that:
                distance = get_manhatandistance(scanner_positions[this][0], scanner_positions[that][0])
                maximum = maximum if maximum > distance else distance
    return len(known_beacons), maximum


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        scanners: Input = []
        scanner: Scanner = (0,[])
        for line in file.readlines():
            line = line.strip()
            if line and line[1] == "-":
                scanner = (int(line.split(" ")[2]), [])
                scanners.append(scanner)
                continue
            if line:
                split = line.split(",")
                scanner[1].append((int(split[0]), int(split[1]), int(split[2])))
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
