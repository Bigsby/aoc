#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Tuple

Scanners = Dict[int, int]


def part1(scanners: Scanners, cycles: Scanners) -> int:
    severity: int = 0
    for current_layer in range(max(scanners.keys()) + 1):
        if current_layer in cycles and current_layer % cycles[current_layer] == 0:
            severity += current_layer * scanners[current_layer]
    return severity


def run_packet_until_caught(cycles: Scanners, offset: int) -> bool:
    for current_layer in range(max(cycles.keys()) + 1):
        if current_layer in cycles and (current_layer + offset) % cycles[current_layer] == 0:
            return False
    return True


def part2(cycles: Scanners):
    offset = 1
    while not run_packet_until_caught(cycles, offset):
        offset += 1
    return offset


def solve(scanners: Scanners) -> Tuple[int, int]:
    cycles = {layer: 2 * (range - 1) for layer, range in scanners.items()}
    return (
        part1(scanners, cycles),
        part2(cycles)
    )


def parse_line(line: str) -> Tuple[int, int]:
    depth, range = line.split(":")
    return int(depth.strip()), int(range.strip())


def get_input(file_path: str) -> Dict[int, int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return {scanner: depth for scanner, depth in map(parse_line, file.readlines())}


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
