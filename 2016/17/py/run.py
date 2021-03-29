#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from hashlib import md5


DIRECTIONS = {
    "U": 1j,
    "D": -1j,
    "L": -1,
    "R": 1
}


def solve(passcode: str) -> Tuple[str, int]:
    queue: List[Tuple[complex, str]] = [(0j, "")]
    longest_path_found = 0
    shortest_path = ""
    while queue:
        room, path = queue.pop(0)
        if room == 3 - 3j:
            if not shortest_path:
                shortest_path = path
            longest_path_found = max(longest_path_found, len(path))
            continue
        path_hash = md5((passcode + path).encode("utf-8")).hexdigest()[:4]
        for index, (path_letter, direction) in enumerate(DIRECTIONS.items()):
            new_room = room + direction
            if path_hash[index] > "a" and 0 <= new_room.real < 4 and -4 < new_room.imag <= 0:
                queue.append((new_room, path + path_letter))
    return shortest_path, longest_path_found


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


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
