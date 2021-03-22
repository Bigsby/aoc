#! /usr/bin/python3

import sys
import os
import time
from typing import Counter, Dict, List, Tuple
import re
from functools import reduce

Record = Tuple[int, List[str]]
Records = Dict[str, Record]


def part1(records: Records) -> str:
    all_children: List[str] = list(
        reduce(lambda acc, children: [*acc, *children[1]], records.values(), []))
    for name in records.keys():
        if name not in all_children:
            return name
    raise Exception("Top not found")


def part2(records: Records, top_tower: str) -> int:
    combined_weights: Dict[str, int] = {}
    while len(combined_weights) != len(records):
        for name, (weight, children) in records.items():
            if name in combined_weights:
                continue
            if not children:
                combined_weights[name] = weight
                continue
            if all(child in combined_weights for child in children):
                combined_weights[name] = reduce(
                    lambda acc, child: acc + combined_weights[child], children, weight)
    current_tower = records[top_tower]
    weight_difference = 0
    while True:
        weight, children = current_tower
        weight_counts = Counter([combined_weights[child]
                                 for child in children])
        if len(weight_counts) == 1:
            return weight + weight_difference
        single_weight: int = next(
            k for k, v in weight_counts.items() if v == 1)
        weight_difference = next(
            k for k, v in weight_counts.items() if v > 1) - single_weight
        next_tower: str = next(
            child for child in current_tower[1] if combined_weights[child] == single_weight)
        current_tower = records[next_tower]


def solve(records: Records) -> Tuple[str, int]:
    top_tower = part1(records)
    return (
        top_tower,
        part2(records, top_tower)
    )


line_regex = re.compile(
    r"^(?P<name>[a-z]+)\s\((?P<weight>\d+)\)(?: -> )?(?P<children>.*)")
def parseLine(line: str) -> Tuple[str, Record]:
    match = line_regex.match(line.strip())
    if match:
        chilren = [child for child in match.group(
            "children").split(", ") if child]
        return match.group("name"), (int(match.group("weight")), chilren)
    else:
        raise Exception("Bad format", line)


def get_input(file_path: str) -> Records:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return {name: record for name, record in map(parseLine, file.readlines())}


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
