#! /usr/bin/python3

import sys, os, time
from hashlib import md5
from typing import Tuple


def find_hash(secret_key: str, prefix_count: int, guess: int) -> int:
    prefix = "0" * prefix_count
    while True:
        hash = md5((secret_key + str(guess)).encode("utf-8")).hexdigest()
        if hash.startswith(prefix):
            return guess
        guess += 1


def solve(secret_key: str) -> Tuple[int,int]:
    part1_result = find_hash(secret_key, 5, 1)
    return (part1_result, find_hash(secret_key, 6, part1_result))


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