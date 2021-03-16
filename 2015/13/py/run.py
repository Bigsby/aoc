#! /usr/bin/python3

import sys
import os
import time
import re
from itertools import permutations
from typing import Dict, Iterable, Tuple

Entries = Dict[str, Dict[str, int]]


def calculate_happiness(arrangement: Tuple[str, ...], entries: Entries) -> int:
    total = 0
    length = len(arrangement)
    for index, person in enumerate(arrangement):
        total += entries[person][arrangement[index - 1]]
        total += entries[person][arrangement[(index + 1) % length]]
    return total


def calculate_maximum_happiness(possible_arragements: Iterable[Tuple[str, ...]], entries: Entries) -> int:
    return max(map(lambda arrangement: calculate_happiness(arrangement, entries), possible_arragements))


def part1(entries: Entries) -> int:
    people = list(entries.keys())
    return calculate_maximum_happiness(permutations(people, len(people)), entries)


def part2(entries: Entries) -> int:
    me = "me"
    entries[me] = {}
    for person in list(entries.keys()):
        if person == me:
            continue
        entries[me][person] = 0
        entries[person][me] = 0
    return part1(entries)


def solve(entries: Entries) -> Tuple[int, int]:
    return (part1(entries), part2(entries))


line_regex = re.compile(
    r"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$")


def get_input(file_path: str) -> Entries:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        entries: Entries = {}
        for line in file.readlines():
            match = line_regex.match(line)
            if match:
                target = match.group(1)
                if target not in entries:
                    entries[target] = {}
                entries[target][match.group(4)] = (1 if match.group(
                    2) == "gain" else -1) * int(match.group(3))
            else:
                raise Exception("Bad format", line)
        return entries


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
