#! /usr/bin/python3

import sys
import os
import time
from typing import Iterable, List, Set, Tuple
import re


Position = complex
ClaySquares = List[Position]
Water = Set[Position]


def get_edges(positions: Iterable[Position]) -> Tuple[int, int, int, int]:
    return int(min(map(lambda s: s.real, positions))), \
        int(max(map(lambda s: s.real, positions))), \
        int(min(map(lambda s: s.imag, positions))), \
        int(max(map(lambda s: s.imag, positions)))


def print_area(clay: ClaySquares, flowing: Water, settled: Water, spring: Position, queue: List[Position], all: bool = False):
    min_x, max_x, min_y, max_y = get_edges(
        clay + list(settled) + list(flowing) + [spring])
    margins = 20
    if not all:
        min_x = max(int(spring.real) - margins * 2, min_x)
        max_x = min(int(spring.real) + margins * 2, max_x)
        min_y = max(int(spring.imag) - margins, min_y)
        max_y = min(int(spring.imag) + margins, max_y)
    for y in range(min_y, max_y + margins + 1):
        for x in range(min_x - margins, max_x + margins + 1):
            c = " "
            position = x + y * 1j
            if position in clay:
                c = "#"
            if position in flowing:
                c = "|"
            if position in settled:
                c = "~"
            if position in queue:
                c = "q"
            if position == spring:
                c = "+"
            print(c, end="")
        print()
    print()


def find_edge(spring: Position, direction: int, settled: Water, clay: ClaySquares) -> Tuple[int, bool]:
    x = direction
    while True:
        current = spring + x
        if current in clay:
            return x - direction, False
        below = current + 1j
        if below not in clay and below not in settled:
            return x, True
        x += direction


def solve(clay: ClaySquares) -> Tuple[int, int]:
    max_y = int(max(map(lambda s: s.imag, clay)))
    min_y = int(min(map(lambda s: s.imag, clay)))
    settled: Water = set()
    flowing: Water = set()
    queue = [500 + min_y * 1j]
    while queue:
        spring = queue.pop()
        below = spring + 1j
        if below in flowing:
            continue
        flowing.add(spring)
        while below.imag <= max_y and below not in clay and below not in settled:
            flowing.add(below)
            below += 1j
        if below in clay or below in settled:
            x, y = int(below.real), below.imag * 1j - 1j
            left_offset, left_overflown = find_edge(
                below - 1j, -1, settled, clay)
            right_offset, right_overflown = find_edge(
                below - 1j, 1, settled, clay)
            is_overflown = left_overflown or right_overflown
            if not is_overflown:
                queue.append(below - 2j)
            for level_x in range(x + left_offset, x + right_offset + 1):
                position = level_x + y
                if is_overflown:
                    flowing.add(position)
                else:
                    settled.add(position)
                    if position in flowing:
                        flowing.remove(position)
                    if position in queue:
                        queue.remove(position)
            if left_overflown:
                queue.append(x + left_offset + y)
            if right_overflown:
                queue.append(x + right_offset + y)
    return len(settled) + len(flowing), len(settled)


line_regex = re.compile(
    r"^(?P<sC>x|y)=(?P<sV>\d+), (?:x|y)=(?P<mS>\d+)..(?P<mE>\d+)$")


def parse_line(line: str) -> ClaySquares:
    match = line_regex.match(line)
    if match:
        result: ClaySquares = []
        sc, sv, ms, me = match.group("sC"), int(match.group("sV")), int(
            match.group("mS")), int(match.group("mE"))
        if sc == "x":
            for y in range(ms, me + 1):
                result.append(sv + y * 1j)
        else:
            for x in range(ms, me + 1):
                result.append(x + sv * 1j)
        return result
    raise Exception("Bad format", line)


def get_input(file_path: str) -> ClaySquares:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        clay: ClaySquares = []
        for line in file.readlines():
            clay += parse_line(line)
        return clay


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
