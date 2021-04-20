#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from collections import defaultdict

Bug = complex
Bugs = List[Bug]
DIRECTIONS = [1, -1, 1j, -1j]


def gets_bug(has_bug: bool, adjacent_count: int) -> bool:
    return adjacent_count == 1 if has_bug else adjacent_count in (1, 2)


def next_minute(bugs: Bugs) -> Bugs:
    new_state: List[Bug] = []
    for y in range(5):
        for x in range(5):
            position = x + y * 1j
            adjacent_count = sum(
                offset + position in bugs for offset in DIRECTIONS)
            if gets_bug(position in bugs, adjacent_count):
                new_state.append(position)
    return new_state


def part1(bugs: Bugs) -> int:
    previous = [bugs]
    while True:
        bugs = next_minute(bugs)
        if bugs in previous:
            break
        previous.append(bugs)
    biodiversity = 0
    for y in range(5):
        for x in range(5):
            if x + y * 1j in bugs:
                biodiversity += 1 << (y * 5 + x)
    return biodiversity


CENTER = 2 + 2j
MIDDLE_TOP = 2 + 1j
MIDDLE_LEFT = 1 + 2j
MIDDLE_RIGHT = 3 + 2j
MIDDLE_BOTTOM = 2 + 3j


def next_layered_minute(layers: Dict[int, Bugs]) -> Dict[int, Bugs]:
    new_state: Dict[int, Bugs] = defaultdict(list)
    for layer in range(min(layers.keys()) - 1, max(layers.keys()) + 2):
        for y in range(5):
            for x in range(5):
                position = x + y * 1j
                if position == CENTER:
                    continue
                adjacent_count = sum(
                    offset + position in layers[layer] for offset in DIRECTIONS)
                if y == 0:
                    adjacent_count += MIDDLE_TOP in layers[layer - 1]
                elif y == 4:
                    adjacent_count += MIDDLE_BOTTOM in layers[layer - 1]

                if x == 0:
                    adjacent_count += MIDDLE_LEFT in layers[layer - 1]
                elif x == 4:
                    adjacent_count += MIDDLE_RIGHT in layers[layer - 1]

                if position == MIDDLE_TOP:
                    adjacent_count += sum(x in layers[layer + 1]
                                          for x in range(5))
                elif position == MIDDLE_LEFT:
                    adjacent_count += sum(y *
                                          1j in layers[layer + 1] for y in range(5))
                elif position == MIDDLE_RIGHT:
                    adjacent_count += sum(4 + y *
                                          1j in layers[layer + 1] for y in range(5))
                elif position == MIDDLE_BOTTOM:
                    adjacent_count += sum(x +
                                          4j in layers[layer + 1] for x in range(5))
                if gets_bug(position in layers[layer], adjacent_count):
                    new_state[layer].append(position)
    return new_state


def part2(bugs: Bugs) -> int:
    layers: Dict[int, Bugs] = defaultdict(list)
    layers[0] = bugs
    for _ in range(200):
        layers = next_layered_minute(layers)
    return sum(len(bugs) for bugs in layers.values())


def solve(bugs: Bugs) -> Tuple[int, int]:
    return (
        part1(bugs),
        part2(bugs)
    )


def get_input(file_path: str) -> Bugs:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        bugs: Bugs = []
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    bugs.append(x + y * 1j)
        return bugs


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
