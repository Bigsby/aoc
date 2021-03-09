#! /usr/bin/python3

import sys, os, time
from typing import Tuple
import re


marker_regex = re.compile(r"(?P<prior>[A-Z]*)\((?P<length>\d+)x(?P<repeats>\d+)\)(?P<data>.*)")
def get_length(data: str, recursive: bool) -> int:
    match = marker_regex.match(data)
    if match:
        data_length = int(match.group("length"))
        data = match.group("data")
        return len(match.group("prior")) + \
            int(match.group("repeats")) * (get_length(data[:data_length], True) if recursive else data_length) + \
            get_length(data[data_length:], recursive)
    else:
        return len(data)


def solve(data: str) -> Tuple[int,int]:
    return (
        get_length(data, False), 
        get_length(data, True)
    )


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