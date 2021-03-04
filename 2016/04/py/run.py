#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from collections import Counter
import re

Room = Tuple[str, int, str]


def is_room_valid(name: str, checksum: str) -> bool:
    name = name.replace("-", "")
    counts: Dict[str, int] = Counter(name)
    processed_checksum = "".join([letter for letter, _ in sorted(
        counts.items(), key=lambda kv: (-kv[1], kv[0]))[:5]])
    return processed_checksum == checksum


A_ORD = ord("a")
Z_ORD = ord("z")
DASH_ORD = ord("-")
SPACE_ORD = ord(" ")
def get_next_char(c: int) -> int:
    if c == DASH_ORD or c == SPACE_ORD:
        return SPACE_ORD
    if c == Z_ORD:
        return A_ORD
    else:
        return c + 1


def rotate_name(name: str, count: int) -> str:
    name_ints = [ord(c) for c in name]
    for _ in range(count):
        for index in range(len(name_ints)):
            name_ints[index] = get_next_char(name_ints[index])
    return "".join([chr(c) for c in name_ints])


SEARCH_NAME = "northpole object storage"
def solve(rooms: List[Room]) -> Tuple[int, int]:
    return (
        sum(id
            for name, id, checksum in rooms
            if is_room_valid(name, checksum)),
        next(id
             for name, id, checksum in rooms
             if is_room_valid(name, checksum) and rotate_name(name, id) == SEARCH_NAME)
    )


line_regex = re.compile(
    r"^(?P<name>[a-z\-]+)-(?P<id>\d+)\[(?P<checksum>\w+)\]$")
def parseLine(line: str) -> Room:
    match = line_regex.match(line)
    if match:
        return match.group("name"), int(match.group("id")), match.group("checksum")
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Room]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parseLine(line) for line in file.readlines()]


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
