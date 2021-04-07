#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple

Position = complex
Tubes = List[Position]
Letters = Dict[Position, str]


def solve(data: Tuple[Tubes, Letters, Position]) -> Tuple[str, int]:
    tubes, letters, current_position = data
    path: List[str] = []
    direction = 1j
    steps = 0
    while True:
        steps += 1
        if current_position in letters:
            path.append(letters[current_position])
        if current_position + direction in tubes:
            current_position += direction
        elif current_position + direction * 1j in tubes:
            direction *= 1j
            current_position += direction
        elif current_position + direction * -1j in tubes:
            direction *= -1j
            current_position += direction
        else:
            break
    return "".join(path), steps


TUBES = ["|", "+", "-"]


def get_input(file_path: str) -> Tuple[Tubes, Letters, Position]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        tubes: Tubes = []
        letters: Letters = {}
        start = -1j
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                position = x + y * 1j
                if c in TUBES:
                    tubes.append(position)
                    if y == 0:
                        start = position
                if "A" <= c <= "Z":
                    letters[position] = c
                    tubes.append(position)
        return tubes, letters, start


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
