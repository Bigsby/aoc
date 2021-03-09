#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple
import re
from collections import deque


def solve(puzzle_input: Tuple[int, int]) -> Tuple[int, int]:
    elves_count, last_marble = puzzle_input
    scores = [0] * elves_count
    circle = deque([0])
    part1_score = 0
    for next_marble in range(1, 1 + last_marble * 100):
        if next_marble == last_marble:
            part1_score = max(scores)
        if next_marble % 23:
            circle.rotate(-1)
            circle.append(next_marble)
        else:
            circle.rotate(7)
            scores[next_marble % elves_count] += next_marble + circle.pop()
            circle.rotate(-1)
    return part1_score, max(scores)


input_regex = re.compile(
    r"^(?P<players>\d+) players; last marble is worth (?P<last>\d+)")


def get_input(file_path: str) -> Tuple[int, int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        match = input_regex.match(file.read())
        if match:
            return int(match.group("players")), int(match.group("last"))
        raise Exception("Bad input")


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
