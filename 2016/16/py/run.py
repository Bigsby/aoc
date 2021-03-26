#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


def get_checksum(data: str, disk_length: int) -> str:
    while len(data) < disk_length:
        data = "0".join(
            [data, "".join(["1" if c == "0" else "0" for c in data[::-1]])])
        print(data); input()
    data = data[:disk_length]
    while len(data) % 2 == 0:
        data = "".join(["1" if data[index] == data[index + 1]
                        else "0" for index in range(0, len(data), 2)])
    return data


def solve(data: str) -> Tuple[str, str]:
    return (
        get_checksum(data, 272),
        get_checksum(data, 35651584)
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
